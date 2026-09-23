#!/usr/bin/env python3
"""Crea la máquina gratuita de VeloDesk en Oracle Cloud reintentando hasta que
haya capacidad ("Out of capacity" es el error habitual de la capa gratuita).

Qué hace, en orden:
  1. Crea la red (VCN, subred pública, puerta de enlace a internet) si no existe,
     con los puertos de VeloDesk abiertos: TCP 22, 21115-21119 y UDP 21116.
  2. Intenta crear la instancia alternando las dos formas Always Free:
     VM.Standard.A1.Flex (ARM, 1 núcleo, 6 GB) y VM.Standard.E2.1.Micro (AMD, 1 GB).
     Si no hay capacidad, espera y vuelve a intentarlo. Ctrl+C para parar.
  3. Cuando arranca, imprime la IP pública, la guarda en server/oracle/instancia.json
     y, con --instalar, ejecuta server/instalar-servidor.sh por SSH.

Requisitos (una sola vez):
  pip install oci
  Clave API en Oracle: Perfil > Mi perfil > Claves API > Añadir clave API >
  pegar ~/.oci/velodesk_api_public.pem y copiar el fragmento de configuración
  en ~/.oci/config (con key_file=~/.oci/velodesk_api.pem).

Uso:
  python server/oracle/reintentar-instancia.py            # solo crear
  python server/oracle/reintentar-instancia.py --instalar # crear + instalar servidor
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time

try:
    import oci
except ImportError:
    sys.exit("Falta el SDK de Oracle: ejecuta  pip install oci")

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
ESTADO = AQUI / "instancia.json"
NOMBRE = "velodesk-server"
SSH_KEY = pathlib.Path.home() / ".ssh" / "velodesk_oracle"
PUERTOS_TCP = [(22, 22), (21115, 21119)]
PUERTOS_UDP = [(21116, 21116)]
FORMAS = [
    ("VM.Standard.A1.Flex", dict(ocpus=1, memory_in_gbs=6)),
    ("VM.Standard.E2.1.Micro", None),
]


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def esperar(cliente, getter, estado):
    return oci.wait_until(cliente, getter, "lifecycle_state", estado, max_wait_seconds=600).data


def preparar_red(net, compartment):
    vcns = [v for v in net.list_vcns(compartment).data if v.display_name == "velodesk-vcn"]
    if vcns:
        vcn = vcns[0]
        log(f"VCN existente: {vcn.id}")
    else:
        log("Creando VCN velodesk-vcn")
        vcn = net.create_vcn(oci.core.models.CreateVcnDetails(
            cidr_block="10.0.0.0/16", compartment_id=compartment,
            display_name="velodesk-vcn", dns_label="velodesk")).data
        vcn = esperar(net, net.get_vcn(vcn.id), "AVAILABLE")

    igws = net.list_internet_gateways(compartment, vcn_id=vcn.id).data
    igw = igws[0] if igws else None
    if igw is None:
        log("Creando puerta de enlace a internet")
        igw = net.create_internet_gateway(oci.core.models.CreateInternetGatewayDetails(
            compartment_id=compartment, vcn_id=vcn.id, is_enabled=True,
            display_name="velodesk-igw")).data
        igw = esperar(net, net.get_internet_gateway(igw.id), "AVAILABLE")

    rt = net.get_route_table(vcn.default_route_table_id).data
    if not any(r.destination == "0.0.0.0/0" for r in rt.route_rules):
        log("Añadiendo ruta por defecto a internet")
        net.update_route_table(rt.id, oci.core.models.UpdateRouteTableDetails(route_rules=[
            oci.core.models.RouteRule(destination="0.0.0.0/0", destination_type="CIDR_BLOCK",
                                      network_entity_id=igw.id)]))

    ingress = []
    for lo, hi in PUERTOS_TCP:
        ingress.append(oci.core.models.IngressSecurityRule(
            protocol="6", source="0.0.0.0/0", source_type="CIDR_BLOCK",
            tcp_options=oci.core.models.TcpOptions(
                destination_port_range=oci.core.models.PortRange(min=lo, max=hi))))
    for lo, hi in PUERTOS_UDP:
        ingress.append(oci.core.models.IngressSecurityRule(
            protocol="17", source="0.0.0.0/0", source_type="CIDR_BLOCK",
            udp_options=oci.core.models.UdpOptions(
                destination_port_range=oci.core.models.PortRange(min=lo, max=hi))))
    ingress.append(oci.core.models.IngressSecurityRule(protocol="1", source="0.0.0.0/0",
                                                       source_type="CIDR_BLOCK"))
    egress = [oci.core.models.EgressSecurityRule(protocol="all", destination="0.0.0.0/0",
                                                 destination_type="CIDR_BLOCK")]
    log("Actualizando lista de seguridad (puertos de VeloDesk)")
    net.update_security_list(vcn.default_security_list_id,
                             oci.core.models.UpdateSecurityListDetails(
                                 ingress_security_rules=ingress, egress_security_rules=egress))

    subnets = [s for s in net.list_subnets(compartment, vcn_id=vcn.id).data
               if s.display_name == "velodesk-subnet"]
    if subnets:
        subnet = subnets[0]
    else:
        log("Creando subred pública")
        subnet = net.create_subnet(oci.core.models.CreateSubnetDetails(
            cidr_block="10.0.0.0/24", compartment_id=compartment, vcn_id=vcn.id,
            display_name="velodesk-subnet", dns_label="velodesk",
            prohibit_public_ip_on_vnic=False)).data
        subnet = esperar(net, net.get_subnet(subnet.id), "AVAILABLE")
    return subnet.id


def imagen_ubuntu(compute, compartment, forma):
    imgs = compute.list_images(compartment, operating_system="Canonical Ubuntu",
                               operating_system_version="24.04", shape=forma,
                               sort_by="TIMECREATED", sort_order="DESC").data
    if not imgs:
        imgs = compute.list_images(compartment, operating_system="Canonical Ubuntu",
                                   shape=forma, sort_by="TIMECREATED", sort_order="DESC").data
    if not imgs:
        raise RuntimeError(f"No hay imagen Ubuntu para {forma}")
    return imgs[0].id


def instancia_existente(compute, compartment):
    for i in compute.list_instances(compartment, display_name=NOMBRE).data:
        if i.lifecycle_state in ("PROVISIONING", "STARTING", "RUNNING"):
            return i
    return None


def ip_publica(compute, net, compartment, instance_id):
    for _ in range(60):
        att = [a for a in compute.list_vnic_attachments(compartment, instance_id=instance_id).data
               if a.lifecycle_state == "ATTACHED"]
        if att:
            vnic = net.get_vnic(att[0].vnic_id).data
            if vnic.public_ip:
                return vnic.public_ip
        time.sleep(5)
    raise RuntimeError("La instancia no tiene IP pública; asígnala desde la consola (VNIC > IP pública efímera)")


def lanzar(compute, compartment, ad, subnet_id, forma, cfg, image_id, pubkey):
    detalles = oci.core.models.LaunchInstanceDetails(
        availability_domain=ad, compartment_id=compartment, shape=forma,
        display_name=NOMBRE,
        source_details=oci.core.models.InstanceSourceViaImageDetails(
            image_id=image_id, boot_volume_size_in_gbs=50),
        create_vnic_details=oci.core.models.CreateVnicDetails(
            subnet_id=subnet_id, assign_public_ip=True, display_name="velodesk-vnic"),
        metadata={"ssh_authorized_keys": pubkey},
    )
    if cfg:
        detalles.shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(**cfg)
    return compute.launch_instance(detalles).data


def instalar(ip):
    script = RAIZ / "server" / "instalar-servidor.sh"
    log(f"Instalando el servidor por SSH en ubuntu@{ip}")
    for intento in range(20):
        r = subprocess.run(
            ["ssh", "-i", str(SSH_KEY), "-o", "StrictHostKeyChecking=accept-new",
             "-o", "ConnectTimeout=15", f"ubuntu@{ip}", "sudo bash -s"],
            stdin=open(script, "rb"))
        if r.returncode == 0:
            return True
        log(f"SSH aún no disponible (intento {intento + 1}); espero 30 s")
        time.sleep(30)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instalar", action="store_true", help="instala el servidor por SSH al terminar")
    ap.add_argument("--espera", type=int, default=120, help="segundos entre reintentos")
    ap.add_argument("--perfil", default="DEFAULT")
    a = ap.parse_args()

    config = oci.config.from_file(profile_name=a.perfil)
    oci.config.validate_config(config)
    compartment = config["tenancy"]
    identity = oci.identity.IdentityClient(config)
    compute = oci.core.ComputeClient(config)
    net = oci.core.VirtualNetworkClient(config)
    pubkey = (SSH_KEY.with_suffix(".pub")).read_text().strip()

    inst = instancia_existente(compute, compartment)
    if inst is None:
        subnet_id = preparar_red(net, compartment)
        ad = identity.list_availability_domains(compartment).data[0].name
        imagenes = {f: imagen_ubuntu(compute, compartment, f) for f, _ in FORMAS}
        intento = 0
        while inst is None:
            forma, cfg = FORMAS[intento % len(FORMAS)]
            intento += 1
            try:
                log(f"Intento {intento}: creando {NOMBRE} con {forma}")
                inst = lanzar(compute, compartment, ad, subnet_id, forma, cfg, imagenes[forma], pubkey)
            except oci.exceptions.ServiceError as e:
                msg = (e.message or "")
                if "Out of capacity" in msg or "Out of host capacity" in msg or e.status == 500:
                    log(f"Sin capacidad para {forma}. Reintento en {a.espera} s")
                    time.sleep(a.espera)
                elif e.status == 429:
                    log("Demasiadas peticiones; espero 5 minutos")
                    time.sleep(300)
                else:
                    raise
    log(f"Instancia {inst.id} en estado {inst.lifecycle_state}; esperando RUNNING")
    inst = esperar(compute, compute.get_instance(inst.id), "RUNNING")
    ip = ip_publica(compute, net, compartment, inst.id)
    ESTADO.write_text(json.dumps({"instance_id": inst.id, "ip": ip, "shape": inst.shape}, indent=2))
    print()
    print("=" * 60)
    print(f" Servidor creado: {inst.shape}")
    print(f" IP pública: {ip}")
    print(f" SSH: ssh -i {SSH_KEY} ubuntu@{ip}")
    print("=" * 60)
    if a.instalar:
        ok = instalar(ip)
        print("Instalación completada" if ok else "No se pudo instalar por SSH; ejecútalo a mano")


if __name__ == "__main__":
    main()

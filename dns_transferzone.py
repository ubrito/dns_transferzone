import argparse
import dns.query
import dns.zone
import re
import socket

def verify_ip_or_name(server):
    
    pattern = r"(((1[0-9]|[1-9]?)[0-9]|2([0-4][0-9]|5[0-5]))\.){3}((1[0-9]|[1-9]?)[0-9]|2([0-4][0-9]|5[0-5]))"
    validate_ip = re.match(pattern, server)
    
    if validate_ip:
        return server
    else:
        try:
            ip = socket.gethostbyname(server)
            return ip
        except Exception:
            return False


def transfer_zone(server, domain):
    
    try:
        return dns.zone.from_xfr(dns.query.xfr(server, domain))
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Busca e transfere Zonas DNS dos Domínios dados")
    parser.add_argument('--server', help='O servidor DNS a ser consultado.', required=True)
    parser.add_argument('--domain', help='O domínio a ser usado na consulta.', required=True)
    parsed = parser.parse_args()

    if verify_ip_or_name(parsed.server):
        results = transfer_zone(verify_ip_or_name(parsed.server), parsed.domain)

        if not results:
            print(results)
            print('Não foi possível transferir a zona.')
        else:
            for name in results.nodes.keys():
                print(results[name].to_text(name))
    
    else:
        print("Servidor não existe")


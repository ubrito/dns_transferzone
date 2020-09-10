import dns.query
import dns.zone
import argparse as ap

def transfer_zone(server, domain):
    try:
        return dns.zone.from_xfr(dns.query.xfr(server, domain))
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':

    parser = ap.ArgumentParser(description="Busca e transfere Zonas DNS dos Domínios dados")
    parser.add_argument('--server', help='O servidor DNS a ser consultado.', required=True)
    parser.add_argument('--domain', help='O domínio a ser usado na consulta.', required=True)
    parsed = parser.parse_args()

    results = transfer_zone(parsed.server, parsed.domain)

    if not results:
        print(results)
        print('Não foi possível transferir a zona.')
    else:
        for name in results.nodes.keys():
            print(results[name].to_text(name))


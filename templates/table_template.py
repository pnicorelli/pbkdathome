def generate_address_table(coin: str, addresses: list[dict]) -> str:
    result = f'<b>{coin}</b><br /><table>'
    result += '<tr><th>wallet</th><th>address</th><th>PK</th></tr>'
    for addr in addresses:
        result += '<tr>'
        result += f'<td>{addr["index"]}</td><td><b>{addr["address"]}</b></td>'
        result += f'<td><b>{addr["private_key"]}</b></td>'
        result += '</tr>'
    result += '</table>'
    return result
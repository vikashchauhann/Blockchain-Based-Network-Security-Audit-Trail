import os
import asyncio
import base64
import json
from datetime import datetime
from mitmproxy import http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons.core import Core
from mitmproxy.options import Options
from web3 import Web3, HTTPProvider

# Set proxy environment variables to point to your proxy server
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:8888'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:8888'

# Bypass proxy for local Ganache instance
os.environ['NO_PROXY'] = '127.0.0.1,localhost'


class RequestLogger:
    def deploy_contract(self, request_info):
        try:
            # Connect to Ganache
            ganache_url = "http://127.0.0.1:7545"  # Ganache URL
            # Create a Web3 instance with a timeout of 60 seconds
            web3 = Web3(HTTPProvider(ganache_url, request_kwargs={'timeout': 60}))

            # Load contract bytecode and ABI
            with open('SmartContracts/SmartContract.bin', 'r') as file:
                bytecode = file.read()
            with open('SmartContracts/SmartContract.abi', 'r') as file:
                abi = json.load(file)

            # Encode request_info as JSON string
            request_info_json_str = json.dumps(request_info)

            # Deploy the contract
            Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
            tx_hash = Contract.constructor(request_info_json_str).transact({'from': web3.eth.accounts[0]})
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            contract_address = tx_receipt.contractAddress
            print("Contract deployed at address:", contract_address)
            return contract_address
        except Exception as e:
            print(f"Error deploying contract: {e}")
            return None

    def format_log_entry(self, flow):
        try:
            # Attempt to decode content assuming it's UTF-8 encoded
            content = flow.request.content.decode("utf-8")
        except UnicodeDecodeError:
            # If decoding fails, encode the content using Base64
            content = base64.b64encode(flow.request.content).decode("utf-8")

        # Extract information from the flow and format it into a dictionary
        request_info = {
            "Method": flow.request.method,
            "URL": flow.request.pretty_url,
            "Headers": dict(flow.request.headers),
            "Content": content,
            "Client IP": flow.client_conn.peername[0],
            "HTTP Status Code": flow.response.status_code if flow.response else None,
            "Timestamp": datetime.now().isoformat(),
            "Referrer": flow.request.headers.get("Referer", ""),
            "Protocol Version": flow.request.http_version,
            "Error Message": flow.error.msg if flow.error else None,
            "Response Headers": dict(flow.response.headers) if flow.response else None,
            "Session ID": flow.request.cookies.get("sessionid", ""),
            "Content Length": flow.response.headers.get("Content-Length", "") if flow.response else "",
            "Content Encoding": flow.response.headers.get("Content-Encoding", "") if flow.response else "",
            "security_headers": self.extract_security_headers(flow.response.headers) if flow.response else None,
        }
        return request_info

    def extract_security_headers(self, headers):
        # Extract relevant security headers from the response headers
        security_headers = {
            "content_security_policy": headers.get("Content-Security-Policy"),
            "x_content_type_options": headers.get("X-Content-Type-Options"),
            "x_xss_protection": headers.get("X-XSS-Protection")
        }
        return security_headers

    def request(self, flow: http.HTTPFlow):
        # Handle HTTP request
        request_info = self.format_log_entry(flow)
        # Deploy a smart contract with the information from the request
        self.deploy_contract(request_info)

    def response(self, flow: http.HTTPFlow):
        # Handle HTTP response
        pass


async def run_proxy():
    # Setup Mitmproxy
    loop = asyncio.get_event_loop()
    options = Options(listen_port=8888)  # Set up proxy listening port
    addons = [
        RequestLogger()  # Add RequestLogger as an addon
    ]
    master = DumpMaster(options, with_termlog=False)
    master.addons.add(*addons)
    try:
        # Run Mitmproxy event loop
        await master.run()
    except KeyboardInterrupt:
        # Shutdown Mitmproxy on keyboard interrupt
        master.shutdown()


if __name__ == "__main__":
    # Run the Mitmproxy
    asyncio.run(run_proxy())

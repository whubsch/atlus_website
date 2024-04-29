export const pyCode = `import requests

add_dict = {"address": "1600 Pennsylvania Ave. NW"}
API_URL = "https://atlus.dev/api/address/parse"
response = requests.post(
  API_URL,
  json=add_dict,
  timeout=10
)`;

export const jsCode = `const url = "https://atlus.dev/api/address/parse";
const addInput = "1600 Pennsylvania Ave. NW";
const myResponse = await fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    accept: "application/json",
  },
  body: JSON.stringify({ address: addInput },
  mode: "cors",
});`;

export const curlCode = `curl -X POST \\
  https://atlus.dev/api/address/parse/ \\
  -H 'accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -d '{
  "address": "1600 Pennsylvania Ave. NW"
}'`;

export const pyCode = `import requests

add_dict = {"address": "1600 Pennsylvania Ave."}
API_URL = "https://atlus.dev/api/address/parse"
response = requests.post(
  API_URL,
  json=add_dict,
  timeout=10
)`;

export const jsCode = `const url = "https://atlus.dev/api/address/parse";
const addInput = "1600 Pennsylvania Ave.";
const myResponse = await fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    accept: "application/json",
  },
  body: JSON.stringify({ address: addInput },
  mode: "cors",
});`;

export const curlCode = `curl -X POST -H "Content-Type: application/json" -d '{"address": "1600 Pennsylvania Ave."}' https://atlus.dev/api/address/parse/`;

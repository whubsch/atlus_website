import { useState } from "react";
import "./App.css";
import { Button, Input, Card, CardBody, Spinner } from "@nextui-org/react";
import CopyAllIcon from "@mui/icons-material/CopyAll";
import SwitchAccessShortcutIcon from "@mui/icons-material/SwitchAccessShortcut";
import CheckIcon from "@mui/icons-material/Check";

function App() {
  const [inputValue, setInputValue] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [copyButton, setCopyButton] = useState<string>("Copy");

  const clearAll = () => {
    setInputValue("");
    setResponse("");
    setCopyButton("Copy");
  };

  const handleRandom = () => {
    setInputValue(
      "1500 Pennsylvania Ave NW, Washington, DC 20220, United States"
    );
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const apiUrl = "http://localhost/api/parse/"; // Replace with your API endpoint
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({ address: inputValue }),
        mode: "cors",
      });

      const data = await response.json();
      const tags = data.data;
      delete tags["@id"];
      setResponse(tags);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const clipboardCopy = () => {
    setCopyButton("Copied");
    const text = Object.entries(response).map(
      ([key, value]) => `${key}=${value}`
    );
    navigator.clipboard.writeText(text.join("\n"));
  };

  return (
    <>
      <div className="flex flex-col justify-center items-center py-20 px-4">
        <img src="/logo_white.png" alt="Atlus logo" className="mb-4 w-1/6" />
        <h1 className="text-3xl font-bold mb-4">Atlus</h1>

        <Card className="p-6 rounded-lg w-1/3 min-w-full md:min-w-80">
          <CardBody>
            <form
              className="flex flex-wrap md:flex-nowrap gap-2"
              onSubmit={!inputValue ? handleRandom : handleSubmit}
            >
              <Input
                type="text"
                size="md"
                label="Address"
                value={inputValue}
                onChange={handleInputChange}
              />
              <Button
                color="primary"
                size="md"
                type="submit"
                className="h-14 w-full md:w-auto"
              >
                {!inputValue ? (
                  <SwitchAccessShortcutIcon />
                ) : (
                  <>{!response ? "Submit" : <Spinner color="default" />}</>
                )}
              </Button>
            </form>
          </CardBody>
        </Card>
        <Card
          className={`p-6 rounded-lg w-1/3 min-w-full md:min-w-80${
            !response ? " hidden" : ""
          }`}
        >
          <div className="flex justify-between gap-2 p-2">
            <Button
              color="default"
              size="sm"
              onClick={clearAll}
              className="w-1/2"
            >
              Clear
            </Button>
            <Button
              color="primary"
              size="sm"
              onClick={clipboardCopy}
              endContent={
                copyButton === "Copied" ? <CheckIcon /> : <CopyAllIcon />
              }
              className="w-1/2"
            >
              {copyButton}
            </Button>
          </div>

          {Object.entries(response).map(([key, value], index) => (
            <Input
              isReadOnly
              type="text"
              size="sm"
              label={key}
              value={value}
              className="p-1"
              key={String(index)}
            />
          ))}
        </Card>
      </div>
    </>
  );
}

export default App;

import { useState } from "react";
import "./App.css";
// import Intro from "./components/Intro";
import {
  Button,
  Input,
  Card,
  CardBody,
  Spinner,
  Listbox,
  ListboxItem,
  Tabs,
  Tab,
} from "@nextui-org/react";

import CopyAllIcon from "@mui/icons-material/CopyAll";
import SwitchAccessShortcutIcon from "@mui/icons-material/SwitchAccessShortcut";
import CheckIcon from "@mui/icons-material/Check";

const strings = [
  "123 Main St, Springfield, IL 62701",
  "1500 Pennsylvania Ave NW, Washington, DC 20220, United States",
  "456 Elm Ave, Anytown, NY 12345",
  "789 Oak Dr, Smallville California, 98765",
  "101 W. Pine St Bigtown Texas 54321",
  "234 Cedar Hwy Suite 2, W. Des Moines, IA",
  "345 MAPLE RD, COUNTRYSIDE, PA 24680-0198",
  "678 MLK Blvd, Suburbia, Ohio 97531",
  "890 St Mary St, Metropolis, GA 86420",
  "111 N.E. Cherry St, Villageton, Michigan 36912",
  "222 NW Pineapple Ave, Beachville, SC 75309",
  "333 Orange Blvd, Riverside Arizona 80203",
  "444 Grape St SE, Hilltop, NV 46895 Unit B",
  "158 S. Thomas Court, Marietta, GA 30008",
  "666 BANANA AVE LAKESIDE NEW MEXICO 36921",
  "777 Strawberry Street, Mountainview, OR 25874",
];

function App() {
  const [inputValue, setInputValue] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [copied, setCopied] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedTab, setSelectedTab] = useState<string | number>("address");

  const tabs = ["address", "phone"];
  const clearAll = () => {
    setInputValue("");
    setResponse("");
    setCopied(false);
  };

  const handleRandom = () => {
    const randomIndex = Math.floor(Math.random() * strings.length);
    setInputValue(strings[randomIndex]);
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const apiUrl = `http://localhost:5000/${selectedTab}/parse/`;
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({ [selectedTab]: inputValue }),
        mode: "cors",
      });

      const data = await response.json();
      const tags = data.data;
      delete tags["@id"];
      setResponse(tags);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleClick = () => {
    if (inputValue.trim() === "") {
      handleRandom();
    } else {
      handleSubmit();
    }
  };

  const clipboardCopy = () => {
    setCopied(true);
    const text = Object.entries(response).map(
      ([key, value]) => `${key}=${value}`
    );
    navigator.clipboard.writeText(text.join("\n"));
  };

  return (
    <div className="flex flex-col justify-center items-center py-20 px-4">
      <img
        src="/logo_white.png"
        alt="Atlus logo"
        className="mb-4 w-2/3 md:w-1/4"
      />
      <h1 className="text-3xl font-bold mb-4">Atlus</h1>

      <div className="relative w-1/2 min-w-full md:min-w-80 md:max-w-1/3">
        <Card className="p-6 z-10 rounded-lg overflow-hidden">
          <CardBody>
            <Tabs
              selectedKey={selectedTab}
              onSelectionChange={setSelectedTab}
              className="place-content-center p-2"
            >
              {tabs.map((tab) => (
                <Tab
                  key={tab}
                  title={tab}
                  className="text-transform capitalize"
                ></Tab>
              ))}
            </Tabs>
            <div className="flex flex-wrap max-sm:hidden md:flex-nowrap gap-2">
              <Input
                type="text"
                size="md"
                label="Input"
                value={inputValue}
                onChange={handleInputChange}
                endContent={
                  <Button
                    color="primary"
                    size="md"
                    className="h-full w-4 md:w-auto"
                    onClick={handleClick}
                  >
                    {!inputValue ? (
                      <SwitchAccessShortcutIcon />
                    ) : (
                      <>{!loading ? "Submit" : <Spinner color="default" />}</>
                    )}
                  </Button>
                }
              />
            </div>
            <div className="flex flex-wrap gap-2 md:hidden">
              <Input
                type="text"
                size="md"
                label="Input"
                value={inputValue}
                onChange={handleInputChange}
              />
              <Button
                color="primary"
                size="md"
                className="h-10 md:h-14 w-full md:w-auto"
                onClick={handleClick}
              >
                {!inputValue ? (
                  <SwitchAccessShortcutIcon />
                ) : (
                  <>{!loading ? "Submit" : <Spinner color="default" />}</>
                )}
              </Button>
            </div>
          </CardBody>
        </Card>
        <Card
          className={`p-6 z-0 rounded-lg inset-x-0 top-0 absolute ${
            !response ? "translate-y-0" : "translate-y-60 md:translate-y-48"
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
              endContent={copied ? <CheckIcon /> : <CopyAllIcon />}
              className="w-1/2"
            >
              {copied ? "Copied" : "Copy"}
            </Button>
          </div>
          <div className="flex flex-wrap">
            <Listbox
              variant="flat"
              aria-label="List displaying parsed address"
              emptyContent={null}
            >
              {Object.entries(response)
                .filter(([key, _]) => key !== "@removed")
                .map(([key, value], index) => (
                  <ListboxItem
                    key={String(index)}
                    description={key}
                    className="cursor-default"
                    textValue={value}
                  >
                    {value}
                  </ListboxItem>
                ))}
            </Listbox>
          </div>
        </Card>
      </div>
      {/* <Intro /> */}
    </div>
  );
}

export default App;

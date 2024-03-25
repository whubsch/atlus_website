import { FormEvent, useState } from "react";
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
  Chip,
} from "@nextui-org/react";

import CopyAllIcon from "@mui/icons-material/CopyAll";
import SwitchAccessShortcutIcon from "@mui/icons-material/SwitchAccessShortcut";
import CheckIcon from "@mui/icons-material/Check";
import ErrorSharpIcon from "@mui/icons-material/ErrorSharp";
import Intro from "./components/Intro";
import LogoHeader from "./components/LogoHeader";

const addr_strs = [
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

const phone_strs = [
  "+1 (909) 2988892",
  "17379089203",
  "1.223.394.3983",
  "282-203-2988",
  "1 902 989 2837",
  "9389209876",
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
    const use_strs = selectedTab === "address" ? addr_strs : phone_strs;
    const randomIndex = Math.floor(Math.random() * use_strs.length);
    setInputValue(use_strs[randomIndex]);
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const urlBase = `${
        window.location.hostname === "localhost" &&
        window.location.protocol === "http:"
          ? window.location.protocol + "//localhost:5000"
          : window.location.origin
      }/api`;
      const apiUrl = `${urlBase}/${selectedTab}/parse/`;
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

  const handleClick = (
    event:
      | React.FormEvent<FormEvent>
      | React.MouseEvent<HTMLButtonElement, MouseEvent>
  ) => {
    event.preventDefault();
    if (inputValue.trim() === "") {
      handleRandom();
    } else {
      handleSubmit();
    }
  };

  const clipboardCopy = () => {
    setCopied(true);
    const text = Object.entries(response)
      .filter(([key, _]) => key !== "@removed")
      .map(([key, value]) => `${key}=${value}`);
    navigator.clipboard.writeText(text.join("\n"));

    setTimeout(() => {
      setCopied(false);
    }, 5000);
  };

  return (
    <>
      <div className="flex flex-col justify-center items-center py-20 px-4 gap-6">
        <LogoHeader />
        <div className="relative w-1/2 min-w-full md:min-w-80 md:max-w-1/3 block">
          <Card className="p-4 z-50 rounded-lg">
            <CardBody className="gap-4">
              <Tabs
                selectedKey={selectedTab}
                onSelectionChange={setSelectedTab}
                className="place-content-center px-2"
              >
                {tabs.map((tab) => (
                  <Tab
                    key={tab}
                    title={tab}
                    className="text-transform capitalize"
                  ></Tab>
                ))}
              </Tabs>
              <form className="flex flex-wrap max-sm:hidden md:flex-nowrap gap-2">
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
                      type={inputValue ? "submit" : "button"}
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
              </form>
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
            className={`p-6 rounded-lg inset-x-0 top-0 absolute z-20 block ${
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
              <div className="flex gap-2 p-2">
                {Object.entries(response)
                  .filter(([key, _]) => key === "@removed")
                  .map(([_, value], index) =>
                    value.map((tag) => (
                      <Chip
                        color="danger"
                        size="sm"
                        startContent={<ErrorSharpIcon />}
                        key={`${value}${index}`}
                      >
                        {tag}
                      </Chip>
                    ))
                  )}
              </div>
            </div>
          </Card>
        </div>
      </div>
      <Intro classes={`${!response ? "translate-y-0" : "translate-y-80"}`} />
    </>
  );
}

export default App;

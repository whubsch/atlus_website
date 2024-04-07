import { FormEvent, useState } from "react";
import "./App.css";
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
  Tooltip,
} from "@nextui-org/react";

import CopyAllIcon from "@mui/icons-material/CopyAll";
import AutoFixHighIcon from "@mui/icons-material/AutoFixHigh";
import CheckIcon from "@mui/icons-material/Check";
import ErrorSharpIcon from "@mui/icons-material/ErrorSharp";
import InfoIcon from "@mui/icons-material/Info";

import Intro from "./components/Intro";
import LogoHeader from "./components/LogoHeader";
import { addr_strs, phone_strs } from "./statics";
import Footer from "./components/Footer";

const version = "0.1.0";

interface responseInt {
  "addr:housenumber"?: string;
  "addr:street"?: string;
  "addr:unit"?: string;
  "addr:city"?: string;
  "addr:postcode"?: string;
  "addr:state"?: string;
  phone?: string;
  "@removed"?: string[];
}

interface metaInt {
  version?: string;
  status?: string;
}

function App() {
  const [inputValue, setInputValue] = useState<string>("");
  const [apiMeta, setApiMeta] = useState<metaInt>({});
  const [response, setResponse] = useState<responseInt>({});
  const [copied, setCopied] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedTab, setSelectedTab] = useState<string | number>("address");

  const urlBase = `${
    window.location.hostname === "localhost" &&
    window.location.protocol === "http:"
      ? window.location.protocol + "//localhost:5000"
      : window.location.origin
  }/api`;

  const tabs = ["address", "phone"];
  const clearAll = () => {
    setInputValue("");
    setResponse({});
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
      const apiUrl = `${urlBase}/${selectedTab}/parse/`;
      const myResponse = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({ [selectedTab]: inputValue }),
        mode: "cors",
      });

      const data = await myResponse.json();
      const tags = data.data;
      delete tags["@id"];
      setResponse(tags);
      setApiMeta(data.meta);
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
      <div className="flex flex-col justify-center items-center py-20 px-4 gap-6 sm:py-44">
        <LogoHeader />
        <div className="relative w-1/2 min-w-full md:min-w-80 md:max-w-1/3 block">
          <Card className="p-4 z-40 rounded-lg">
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
                  />
                ))}
              </Tabs>
              <form className="flex flex-wrap max-md:hidden md:flex-nowrap gap-2">
                {/* large screen, button inside */}
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
                        <AutoFixHighIcon />
                      ) : (
                        <>{!loading ? "Submit" : <Spinner color="default" />}</>
                      )}
                    </Button>
                  }
                />
              </form>
              <form className="flex flex-wrap gap-2 md:hidden">
                {/* small screen, button below */}
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
                  type={inputValue ? "submit" : "button"}
                  className="h-10 md:h-14 w-full md:w-auto"
                  onClick={handleClick}
                >
                  {!inputValue ? (
                    <AutoFixHighIcon />
                  ) : (
                    <>{!loading ? "Submit" : <Spinner color="default" />}</>
                  )}
                </Button>
              </form>
            </CardBody>
          </Card>
          <Card
            className={`p-6 rounded-lg inset-x-0 top-0 z-20 block ${
              Object.keys(response).length === 0
                ? "translate-y-0 absolute"
                : "translate-y-4"
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
              <div
                className={`flex gap-2 p-2${
                  response["@removed"]?.length === 0 && " hidden"
                }`}
              >
                {response["@removed"] &&
                  response["@removed"].map((tag: string) => (
                    <Chip
                      color="danger"
                      size="sm"
                      startContent={<ErrorSharpIcon />}
                      key={`${tag}`}
                    >
                      {tag}
                    </Chip>
                  ))}
              </div>
              {apiMeta?.status === "OK" && (
                <>
                  <div className="absolute bottom-0 right-0 max-md:hidden p-3">
                    <Tooltip content={`API version ${apiMeta?.version}`}>
                      <Button size="sm">
                        <InfoIcon />
                      </Button>
                    </Tooltip>
                  </div>
                  <div className="absolute bottom-0 right-0 md:hidden p-3">
                    <Chip size="sm" startContent={<InfoIcon />}>
                      {apiMeta?.version}
                    </Chip>
                  </div>
                </>
              )}
            </div>
          </Card>
        </div>
      </div>
      <Intro classes={`${Object.keys(response).length === 0 && ""}`} />
      <Footer version={version} />
    </>
  );
}

export default App;

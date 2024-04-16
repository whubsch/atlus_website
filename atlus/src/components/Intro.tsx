import HistoryToggleOffIcon from "@mui/icons-material/HistoryToggleOff";
import FactCheckIcon from "@mui/icons-material/FactCheck";
import ApiIcon from "@mui/icons-material/Api";
import IntegrationInstructionsIcon from "@mui/icons-material/IntegrationInstructions";
import { Tab, Tabs } from "@nextui-org/react";

import Perk from "./Perks";
import React from "react";
import { jsCode, curlCode, pyCode } from "./JsCode";
import CodeBlock from "./CodeBlock";
interface SubComponentProps {
  classes?: string;
}

const Intro: React.FC<SubComponentProps> = ({ classes }) => {
  const [selected, setSelected] = React.useState<string | number>("python");

  return (
    <div className={`${classes} z-10 justify-center items-center`}>
      <div className="mx-auto px-4 sm:px-6 lg:px-8 md:w-2/3 p-4 md:p-10">
        <div className="flex max-sm:flex-col sm:flex-wrap max-sm:items-center gap-8">
          <div className="w-4/5 sm:w-2/5">
            <h3 className="text-xl text-deepindigo font-extrabold sm:text-xl">
              Atlus
            </h3>

            <h2 className="text-3xl font-extrabold sm:text-4xl headline">
              The ultimate address parsing solution
            </h2>
            <p>
              Struggling to accurately parse tags from external datasets for
              your mapping projects? Look no further! Atlus is your all-in-one
              solution to effortlessly parsing raw address and phone strings
              into OpenStreetMap-compatible tags.
            </p>
          </div>
          <div className="w-4/5 sm:w-1/2 min-h-96">
            <Tabs
              selectedKey={selected}
              onSelectionChange={setSelected}
              variant="underlined"
            >
              <Tab key="python" title="Python">
                <CodeBlock code={pyCode} language={"python"} />
              </Tab>
              <Tab key="javascript" title="JavaScript">
                <CodeBlock code={jsCode} language={"javascript"} />
              </Tab>
              <Tab key="curl" title="cURL">
                <CodeBlock code={curlCode} language={"bash"} />
              </Tab>
            </Tabs>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap gap-8 md:gap-14 py-6 sm:py-8 lg:py-10 px-4 sm:px-6 lg:px-8 place-content-center">
        <Perk
          title={"efficient"}
          icon={<HistoryToggleOffIcon />}
          description={
            "Save time parsing address strings using Atlus's parsing engine, and leave more time for mapping."
          }
        />
        <Perk
          title={"consistent"}
          icon={<FactCheckIcon className="justify-center" />}
          description={
            "Get consistent tag output, compatible with OSM, regardless of the quality of the input data."
          }
        />
        <Perk
          title={"accessible"}
          icon={<ApiIcon className="justify-center" />}
          description={
            "Access the powers of Atlus using a public API so that you can automate your workflow and work with bigger datasets quickly."
          }
        />
        <Perk
          title={"documented"}
          icon={<IntegrationInstructionsIcon className="justify-center" />}
          description={
            "Follow the clear and auto-generated documentation to get a consistent and reliable output."
          }
        />
      </div>
    </div>
  );
};
export default Intro;

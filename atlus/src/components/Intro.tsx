import HistoryToggleOffIcon from "@mui/icons-material/HistoryToggleOff";
import FactCheckIcon from "@mui/icons-material/FactCheck";
import ApiIcon from "@mui/icons-material/Api";
import { Divider } from "@nextui-org/react";
import Perk from "./Perks";
interface SubComponentProps {
  classes?: string;
}

const Intro: React.FC<SubComponentProps> = ({ classes }) => {
  return (
    <div className={`${classes} z-10 justify-center items-center`}>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 md:w-2/3 p-4 md:p-10">
        <Divider className="m-4 mb-8" />

        <h2 className="text-3xl text-center leading-9 font-extrabold sm:text-4xl sm:leading-10 headline">
          Introducing Atlus: Your Ultimate Address Parsing Solution!
        </h2>
        <p className="mt-3 text-xl text-center leading-7 sm:mt-4">
          Struggling to accurately parse tags from external datasets for your
          mapping projects? Look no further! Atlus is your all-in-one solution
          to effortlessly parsing raw address and phone strings into
          OpenStreetMap-compatible tags.
        </p>
      </div>
      <div className="flex flex-wrap gap-8 md:gap-14 py-6 sm:px-8 lg:px-10 px-4 sm:px-6 lg:px-8 place-content-center">
        <Perk
          title={"efficient"}
          icon={<HistoryToggleOffIcon sx={{ fontSize: "4em" }} />}
          description={
            "Save time parsing address strings using Atlus's parsing engine, and leave more time for mapping."
          }
        />
        <Perk
          title={"consistent"}
          icon={
            <FactCheckIcon
              className="justify-center"
              sx={{ fontSize: "4em" }}
            />
          }
          description={
            "Get consistent tag output, compatible with OSM, regardless of the quality of the input data."
          }
        />
        <Perk
          title={"accessible"}
          icon={<ApiIcon className="justify-center" sx={{ fontSize: "4em" }} />}
          description={
            "Access the powers of Atlus using a public API so that you can automate your workflow and work with bigger datasets quickly."
          }
        />
      </div>
    </div>
  );
};
export default Intro;

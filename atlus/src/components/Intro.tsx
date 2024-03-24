import HistoryToggleOffIcon from "@mui/icons-material/HistoryToggleOff";
import FactCheckIcon from "@mui/icons-material/FactCheck";
import { Divider } from "@nextui-org/react";
interface SubComponentProps {
  classes?: string;
}

const Intro: React.FC<SubComponentProps> = ({ classes }) => {
  return (
    <div className={`${classes} z-10 justify-center items-center`}>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 md:w-2/3">
        <Divider className="m-4 mb-8" />

        <h2 className="text-3xl text-center leading-9 font-extrabold sm:text-4xl sm:leading-10 headline">
          Introducing Atlus: Your Ultimate Address Parsing Solution!
        </h2>
        <p className="mt-3 text-xl text-center leading-7 sm:mt-4">
          Struggling to accurately tag addresses for your mapping projects? Look
          no further! Atlus is your all-in-one solution for effortlessly parsing
          raw address strings into OpenStreetMap-compatible tags.
        </p>
      </div>
      <div className="flex flex-wrap gap-8 max-w-4xl py-6 px-4 sm:px-6 lg:px-8 text-justify justify-center">
        <div className="md:w-1/3 flex flex-col justify-center items-center gap-2">
          <HistoryToggleOffIcon sx={{ fontSize: "4em" }} />
          <p>
            With Atlus, simply input your raw address data, and let our advanced
            algorithms do the heavy lifting. Our intelligent parsing technology
            meticulously analyzes each address, extracting vital components such
            as street names, city names, postal codes, and more, all seamlessly
            compatible with OpenStreetMap standards.
          </p>
        </div>
        <div className="md:w-1/3 flex flex-col justify-center items-center gap-2">
          <FactCheckIcon sx={{ fontSize: "4em" }} />
          <p>
            Say goodbye to tedious manual tagging and hello to streamlined
            efficiency. Whether you're managing large-scale mapping projects,
            optimizing logistics operations, or enhancing location-based
            services, Atlus empowers you to unlock the full potential of your
            address data with unparalleled accuracy and speed.
          </p>
        </div>
      </div>
    </div>
  );
};
export default Intro;

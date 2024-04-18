import LogoSvg from "./LogoSvg";

interface LogoHeaderProps {
  dark: boolean;
}

const LogoHeader: React.FC<LogoHeaderProps> = ({ dark }) => {
  return (
    <div className="py-4">
      <div className="max-sm:hidden flex flex-row gap-6 place-content-center items-center">
        <LogoSvg color={dark ? "white" : "#11181C"} className="mb-4 w-20" />
        <h1 className="text-7xl font-bold mb-4 headline">Atlus</h1>
      </div>
      <div className="sm:hidden flex flex-col items-center justify-center">
        <LogoSvg
          color={dark ? "white" : "#11181C"}
          className="mb-4 h-24 md:w-1/4"
        />
        <h1 className="text-5xl font-bold mb-4 headline">Atlus</h1>
      </div>
    </div>
  );
};

export default LogoHeader;

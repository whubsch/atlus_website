interface LogoSvgProps {
  color: string;
  className: string;
}

const LogoSvg: React.FC<LogoSvgProps> = ({ color, className }) => {
  return (
    <svg
      viewBox="0 0 0.6 0.667"
      fill={color}
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <path d="M.3 0C.28 0 .26.011.25.033l-.244.55c-.023.05.027.102.073.077L.276.555a.051.051 0 0 1 .048 0L.521.66C.567.685.617.633.594.583L.35.033A.054.054 0 0 0 .3 0Zm0 .182c.004 0 .006.003.007.005l.12.266a.008.008 0 0 1-.01.01L.302.433l-.12.03a.008.008 0 0 1-.007-.01C.216.366.254.276.293.187c0-.003.004-.006.008-.005z" />
    </svg>
  );
};
export default LogoSvg;

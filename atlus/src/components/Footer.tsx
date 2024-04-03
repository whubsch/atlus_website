import { Link, Divider } from "@nextui-org/react";

interface FooterProps {
  version: string;
}

const Footer: React.FC<FooterProps> = ({ version }) => {
  // Define your external links and version number here
  const externalLinks = [
    { label: "GitHub", url: "https://github.com/whubsch/atlus" },
    {
      label: "OpenStreetMap",
      url: "https://www.openstreetmap.org/user/whammo",
    },
  ];

  return (
    <div>
      <Divider />
      <div className="flex justify-between items-center p-4 md:p-6">
        <p>© {new Date().getFullYear()} Atlus.</p>
        <div className="md:flex gap-2">
          {externalLinks.map((link, index) => (
            <Link
              key={index}
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              {link.label}
            </Link>
          ))}
          <p>Version {version}</p>
        </div>
      </div>
    </div>
  );
};

export default Footer;

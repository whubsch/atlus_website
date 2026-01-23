import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
} from "@heroui/react";
import GitHubIcon from "@mui/icons-material/GitHub";

const urlBase =
  import.meta.env.VITE_API_URL ||
  `https://cibzhvfi41.execute-api.us-east-1.amazonaws.com/prod/api`;

export default function AtlusNav() {
  return (
    <Navbar className="z-50">
      <NavbarBrand>
        <p className="font-bold text-inherit headline">Atlus</p>
      </NavbarBrand>
      <NavbarContent justify="end">
        <NavbarItem>
          <Link href="https://github.com/whubsch/atlus">
            <GitHubIcon className="text-deepindigo" />
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Button
            as={Link}
            href={`${urlBase}/docs`}
            className="bg-deepindigo text-white"
          >
            Docs
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}

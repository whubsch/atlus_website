import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
} from "@heroui/react";
import GitHubIcon from "@mui/icons-material/GitHub";

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
            href="https://cibzhvfi41.execute-api.us-east-1.amazonaws.com/prod/docs"
            className="bg-deepindigo text-white"
          >
            Docs
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}

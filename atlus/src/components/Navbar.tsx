import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
} from "@nextui-org/react";
import GitHubIcon from "@mui/icons-material/GitHub";

export default function AtlusNav() {
  return (
    <Navbar className="z-50">
      <NavbarBrand>
        <p className="font-bold text-inherit headline">Atlus</p>
      </NavbarBrand>
      <NavbarContent justify="end">
        <NavbarItem className="hidden lg:flex">
          <Link href="https://github.com/whubsch/atlus">
            <GitHubIcon className="text-deepindigo" />
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Button as={Link} href="/docs" className="bg-deepindigo">
            Docs
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}

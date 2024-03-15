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
    <Navbar>
      <NavbarBrand>
        <p className="font-bold text-inherit">Atlus</p>
      </NavbarBrand>
      <NavbarContent justify="end">
        <NavbarItem className="hidden lg:flex">
          <Link href="https://github.com/whubsch/atlus">
            <GitHubIcon />
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Button
            as={Link}
            color="primary"
            href="http://localhost/docs"
            variant="flat"
          >
            Docs
          </Button>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
}

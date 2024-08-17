import { Code, Button, Link } from "@nextui-org/react";

import React from "react";

const Pip: React.FC = () => {
  return (
    <div className="flex max-sm:flex-col sm:flex-wrap max-sm:items-center gap-4">
      <div className="w-4/5 sm:w-1/2 flex flex-col items-center gap-4 p-4">
        <Code size="lg">pip install atlus</Code>
        <Button
          color="primary"
          as={Link}
          href="https://pypi.org/project/atlus/"
          isExternal={true}
          className="bg-deepindigo"
        >
          View on PyPI
        </Button>
      </div>

      <div className="w-4/5 sm:w-2/5">
        <h3 className="text-xl text-deepindigo font-extrabold sm:text-xl">
          Use offline
        </h3>

        <h2 className="text-3xl font-extrabold sm:text-4xl headline">
          Install via pip
        </h2>
        <p>
          Use the power of Atlus on your next project. Atlus is also available
          as a Python package, so you can harness its capabilities without
          making endless API calls.
        </p>
      </div>
    </div>
  );
};
export default Pip;

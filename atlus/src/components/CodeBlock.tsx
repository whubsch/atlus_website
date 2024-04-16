import { Button } from "@nextui-org/react";
import { useState } from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { ocean } from "react-syntax-highlighter/dist/esm/styles/hljs";
import CopyAllIcon from "@mui/icons-material/CopyAll";
import CheckIcon from "@mui/icons-material/Check";

interface CodeBlockProps {
  code: string;
  language: string;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ code, language }) => {
  const [copied, setCopied] = useState<boolean>(false);

  const clipboardCopy = () => {
    setCopied(true);
    navigator.clipboard.writeText(code);

    setTimeout(() => {
      setCopied(false);
    }, 5000);
  };

  return (
    <div className="relative">
      <SyntaxHighlighter
        language={language}
        style={ocean}
        customStyle={{ borderRadius: "0.5rem" }}
      >
        {code}
      </SyntaxHighlighter>
      <Button
        isIconOnly
        size="sm"
        color="default"
        onClick={clipboardCopy}
        className="absolute top-2 right-2 opacity-80"
      >
        {copied ? <CheckIcon /> : <CopyAllIcon />}
      </Button>
    </div>
  );
};
export default CodeBlock;

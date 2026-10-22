import { yaml } from "@codemirror/lang-yaml";
import CodeMirror from "@uiw/react-codemirror";

const extensions = [yaml()];

export function YamlEditor({
  value,
  onChange,
}: {
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <CodeMirror
      className="yaml-editor"
      value={value}
      onChange={onChange}
      extensions={extensions}
      basicSetup={{ foldGutter: true, highlightActiveLine: true }}
      aria-label="Design file (YAML)"
    />
  );
}

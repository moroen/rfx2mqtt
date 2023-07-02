import _ from "lodash";
import _ from "htmx.org";

function component() {
  const element = document.createElement("div");
  element.innerHTML = _.join(["Hello", "lodash"], " ");
  return element;
}
document.body.appendChild(component());

const refP = document.querySelector("#references > p");
let refList = document.querySelectorAll("sup[ref]");

const refAttributes = ["author", "date", "src"];

let refNum = 1;

for (const ref of refList) {
    ref.removeAttribute("ref");

    let attributes = {};

    for (const attribute of ref.attributes) {
        attributes[attribute.name] = attribute.value;
        ref.removeAttribute(attribute.name);
        console.log("COOKED");
    }

    ref.innerHTML = `<a href="${attributes.src}" target="_blank" rel="noopener noreferrer">[${refNum}]</a>`;

    refP.innerHTML += `<br /><sup>[${refNum}]</sup> ${attributes.author}`;

    refNum++;
}

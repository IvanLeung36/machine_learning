const refP = document.querySelector("#references > p");
let refList = document.querySelectorAll("sup[ref]");

// const refAttributes = ["author", "date", "src"];

let refNum = 1;

let refPinnerHTMLList = [];

for (const ref of refList) {
    ref.removeAttribute("ref");

    let attributes = {};

    console.log(ref.attributes);

    for (const attribute of ref.attributes) {
        attributes[attribute.name] = attribute.value;
    }

    while (ref.attributes.length > 0) ref.removeAttribute(ref.attributes[0].name);

    ref.innerHTML = `<a href="${attributes.src}" target="_blank" rel="noopener noreferrer">[${refNum}]</a>`;

    refPinnerHTMLList.push(`<sup>[${refNum}]</sup> From ${attributes.author}, taken at ${attributes.date}`);
    console.log(attributes);

    refNum++;
}

refP.innerHTML += refPinnerHTMLList.join("<br />");

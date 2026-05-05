async function UpdateConversion() {
    const base = document.getElementById("baseCurr").value;
    const target = document.getElementById("conCurr").value;
    const amount = document.getElementById("baseAmount").value;

    // if (!amount || base === target) {
    //     document.getElementById("converted").innerText = "";
    //     return;
    // }
    console.log("FML")
    const response = await fetch(`/api/exchange/${base}/${target}/${amount}`);
    const data = await response.json();

    //console.log(response)
    document.getElementById("converted").innerText = `${amount} ${base} = ${data["convertedValue"]} ${target}`;
}

//document.getElementById("baseCurr").addEventListener("change", updateConversion);
//document.getElementById("conCurr").addEventListener("change", updateConversion);
//document.getElementById("baseAmount").addEventListener("input", updateConversion);

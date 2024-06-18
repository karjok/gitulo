function goselinex(){
	const citeTexts = [...new Set(Array.from(document.getElementsByTagName("cite")).map(cite => cite.textContent.split(" ")[0]))];
	const textToSave = citeTexts.join('\n');
	const blob = new Blob([textToSave], { type: 'text/plain' });
	const link = document.createElement('a');
	const randomName = prompt("file name: ");
	link.download = randomName;
	link.href = window.URL.createObjectURL(blob);
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);
}

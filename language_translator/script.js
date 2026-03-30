async function translateText() {
  const text = document.getElementById("inputText").value.trim();
  const source = document.getElementById("sourceLang").value;
  const target = document.getElementById("targetLang").value;
  const output = document.getElementById("outputText");

  if (!text) {
    alert("Please enter text");
    return;
  }

  output.value = "Translating...";

  try {
    const response = await fetch(
      `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${source}|${target}`
    );

    const data = await response.json();

    if (data.responseStatus !== 200) {
      output.value = "";
      alert(data.responseDetails || "Translation failed");
      return;
    }

    output.value = data.responseData.translatedText;
  } catch (error) {
    console.log("Error:", error);
    output.value = "";
    alert("Translation failed. Check your internet connection.");
  }
}

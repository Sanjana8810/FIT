// ========================================
// FITBOT AI SMART PLATE SCANNER
// One photo -> Multiple foods -> Nutrition
// ========================================

const imageInput = document.getElementById("food-image");
const imagePreview = document.getElementById("image-preview");
const uploadStatus = document.getElementById("upload-status");
const scanButton = document.getElementById("analyze-food");
const nutritionResult = document.getElementById("nutrition-result");

let selectedImage = null;
let previewURL = null;


// 1. IMAGE UPLOAD AND PREVIEW

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    selectedImage = null;
    nutritionResult.replaceChildren();

    if (previewURL) {
        URL.revokeObjectURL(previewURL);
        previewURL = null;
    }

    imagePreview.hidden = true;

    if (!file) {
        uploadStatus.textContent = "Please select a food photograph.";
        return;
    }

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ];

    if (!allowedTypes.includes(file.type)) {
        uploadStatus.textContent =
            "Please select a JPG, PNG or WEBP image.";
        imageInput.value = "";
        return;
    }

    if (file.size > 8 * 1024 * 1024) {
        uploadStatus.textContent =
            "Please choose an image smaller than 8 MB.";
        imageInput.value = "";
        return;
    }

    selectedImage = file;

    previewURL = URL.createObjectURL(file);

    imagePreview.src = previewURL;
    imagePreview.hidden = false;

    uploadStatus.textContent =
        "Photograph uploaded! Ready for AI analysis.";

});


// 2. SEND PHOTO TO FLASK AND GEMINI

scanButton.addEventListener("click", async function () {

    if (!selectedImage) {
        showMessage("Please upload a food photograph first.");
        return;
    }

    const formData = new FormData();

    formData.append("image", selectedImage);

    scanButton.disabled = true;
    scanButton.textContent = "Analysing your plate...";

    showMessage("FITBOT AI is identifying your food items...");

    try {

        const response = await fetch("/scan-food", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Food analysis failed."
            );
        }

        if (!data.items || data.items.length === 0) {
            showMessage(
                "No food items were identified. Please try a clearer photograph."
            );
            return;
        }

        displayNutrition(data);

    } catch (error) {

        console.error("FITBOT Scanner Error:", error);

        showMessage(
            "Scanner error: " + error.message
        );

    } finally {

        scanButton.disabled = false;
        scanButton.textContent = "Scan My Food Plate";

    }

});


// 3. DISPLAY MESSAGES

function showMessage(message) {

    const paragraph = document.createElement("p");

    paragraph.className = "scanner-message";
    paragraph.textContent = message;

    nutritionResult.replaceChildren(paragraph);

}


// 4. DISPLAY AI FOOD ANALYSIS

function displayNutrition(data) {

    const card = document.createElement("div");

    card.className = "nutrition-card";

    const heading = document.createElement("h2");

    heading.textContent = "Your AI Plate Analysis";

    card.appendChild(heading);


    // Individual food items

    const tableWrapper = document.createElement("div");

    tableWrapper.className = "nutrition-table-wrapper";

    const table = document.createElement("table");

    table.className = "nutrition-table";

    const thead = document.createElement("thead");

    const headerRow = document.createElement("tr");

    ["Food Item", "Weight", "Calories", "Confidence"]
        .forEach(label => {

            const th = document.createElement("th");

            th.textContent = label;

            headerRow.appendChild(th);

        });

    thead.appendChild(headerRow);
    table.appendChild(thead);


    const tbody = document.createElement("tbody");

    data.items.forEach(item => {

        const row = document.createElement("tr");

        const values = [
            item.food_name,
            item.estimated_grams + " g",
            item.calories + " kcal",
            item.confidence
        ];

        values.forEach(value => {

            const cell = document.createElement("td");

            cell.textContent = value;

            row.appendChild(cell);

        });

        tbody.appendChild(row);

    });

    table.appendChild(tbody);
    tableWrapper.appendChild(table);

    card.appendChild(tableWrapper);


    // Total calories

    const divider = document.createElement("hr");

    card.appendChild(divider);

    const totalHeading = document.createElement("h2");

    totalHeading.textContent = "Total Plate Nutrition";

    card.appendChild(totalHeading);


    const calorieValue = document.createElement("h1");

    calorieValue.className = "calorie-value";

    calorieValue.textContent =
        Number(data.total_calories).toLocaleString() + " kcal";

    card.appendChild(calorieValue);


    const grams = document.createElement("p");

    grams.innerHTML = "<strong>Total estimated weight:</strong> ";

    grams.appendChild(
        document.createTextNode(data.total_grams + " grams")
    );

    card.appendChild(grams);


    // Notes

    const notes = document.createElement("p");

    notes.textContent = data.notes || "";

    card.appendChild(notes);


    const disclaimer = document.createElement("p");

    disclaimer.className = "scanner-disclaimer";

    disclaimer.textContent =
        data.disclaimer ||
        "Nutrition and weight values are estimates.";

    card.appendChild(disclaimer);


    // Allow user to scan another plate

    const resetButton = document.createElement("button");

    resetButton.type = "button";

    resetButton.textContent = "Scan Another Plate";

    resetButton.addEventListener("click", function () {

        imageInput.value = "";
        selectedImage = null;

        imagePreview.hidden = true;
        imagePreview.removeAttribute("src");

        if (previewURL) {
            URL.revokeObjectURL(previewURL);
            previewURL = null;
        }

        uploadStatus.textContent =
            "Upload your complete food plate";

        nutritionResult.replaceChildren();

    });

    card.appendChild(resetButton);

    nutritionResult.replaceChildren(card);

}
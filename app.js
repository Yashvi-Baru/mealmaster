const appId = "4e48330f";
const appKey = "4a90c8262be9fd8e11f7d84b30b6df4b";
const baseUrl = `https://api.edamam.com/api/recipes/v2?type=public&app_id=${appId}&app_key=${appKey}`;

const recipeContainer = document.querySelector("#recipe-container");
const txtSearch = document.querySelector("#txtSearch");
const btnFind = document.querySelector(".btn");

btnFind.addEventListener("click", () => loadRecipes(txtSearch.value));
txtSearch.addEventListener("keyup", (e) => {
    const inputVal = txtSearch.value;
    if (e.keyCode === 13) {
        loadRecipes(inputVal);
    }
});


const setScrollPosition = () => {
    recipeContainer.scrollTo({ top: 0, behavior: "smooth" });
}

function loadRecipes(type = "panner") {
    const url = baseUrl + `&q=${type}`;
    fetch(url)
        .then((res) => res.json())
        .then((data) => renderRecipes(data.hits))
        .catch((error) => console.log(error))
        .finally(() => setScrollPosition());
}

const renderRecipes = (recipeList = []) => {
    recipeContainer.innerHTML = "";
    recipeList.forEach(recipeObj => {
        const {
            label: recipeTitle,
            ingredientLines,
            image: recipeImage,
        } = recipeObj.recipe;
        const recipeStepsStr = getRecipeStepsStr(ingredientLines);
        const htmlStr = `<div class="recipe">
            <div class="recipe-title">${recipeTitle}</div>
            <div class="recipe-image">
                <img src="${recipeImage}">
            </div>
            <div class="recipe-text">
                <ul>${recipeStepsStr}</ul>
            </div>
        </div>`;
        recipeContainer.insertAdjacentHTML("beforeend", htmlStr);
    });
};

const getRecipeStepsStr = (ingredientLines = []) => {
    let str = "";
    for (var step of ingredientLines) {
        str = str + `<li>${step}</li>`;
    }
    return str;
}

async function searchRecipes() {
    const ingredients = document.querySelector('.search-bar').value;

    if (ingredients.trim() === "") {
        alert("Please enter some ingredients to search for recipes.");
        return; 
    }

    console.log("Searching for recipes with ingredients:", ingredients);

    try {
        const response = await fetch(`http://127.0.0.1:8000/recipes/suggest?user_input=${encodeURIComponent(ingredients)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch recipes'); 
        }

        const recipes = await response.json();
        
        const resultsElement = document.getElementById('recipe-results');
        resultsElement.innerHTML = ''; 

        if (Array.isArray(recipes) && recipes.length === 0) {
            resultsElement.innerHTML = '<li>No recipes found for the given ingredients.</li>';
        } else {
            recipes.forEach(recipe => {
                const card = document.createElement('div');
                card.classList.add('recipe-card');

                card.innerHTML = `
                    <h3>${recipe.name}</h3>
                    <p><strong>Cuisine:</strong> ${recipe.cuisine}</p>
                    <p><strong>Time Estimate:</strong> ${recipe.time_estimate} minutes</p>
                    <p><strong>Instructions:</strong> ${recipe.instructions}</p>
                    <p><strong>History:</strong> ${recipe.history}</p>
                    <h4>Ingredients:</h4>
                    <ul>
                        ${(recipe.ingredients || []).map(ingredient => `<li>${ingredient.ingredient_name} - ${ingredient.quantity || ''}</li>`).join('')}
                    </ul>
                `;

                resultsElement.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Error fetching recipes:', error);
        alert('An error occurred while searching for recipes. Please try again later.');
    }
}

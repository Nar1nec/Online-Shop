async function searchProducts() {
    try {
        var searchQuery = document.getElementsByName("search_query")[0];
        var formData = new FormData();
        formData.append('name_product', searchQuery.value);
        console.log(searchQuery.value);

        const response = await fetch('/admin/products/get_products', {
            method: 'POST',
            body: {'name_product': searchQuery.value},
        });

        if (response.ok) {
            const result = await response.json();
            console.log(result);

            // Assuming you have an existing <ul> element with the id "productList"
            const productList = document.getElementById("productList");

            // Clear existing content
            productList.innerHTML = "";

            // Append each product to the list
            result.forEach(product => {
                const listItem = document.createElement("li");
                listItem.textContent = `${product.name} - ${product.price}`;
                productList.appendChild(listItem);
            });
        } else {
            console.error('Server error:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

async function addProduct() {
    const name = document.getElementById("name").value;
    const price = parseFloat(document.getElementById("price").value);
    const description = document.getElementById("description").value;
    const image_path = document.getElementById("image_path").value;
    const category_id = parseInt(document.getElementById("category_id").value);

    const data = {
      name: name,
      price: price,
      description: description,
      image_path: image_path,
      category_id: category_id,
    };

    const response = await fetch('/admin/products/add_products', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    console.log(result);
  }

  function deleteProduct() {
        var form = document.getElementById('deleteForm');
        var formData = new FormData(form);

        fetch(form.action, {
            method: 'DELETE',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Обработка успешного удаления
        })
        .catch(error => {
            // Обработка ошибок
            console.error('There has been a problem with your fetch operation:', error);
        });
    }
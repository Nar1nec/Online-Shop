async function addCat() {
    const name = document.getElementById("category_name").value;

    console.log(name);
    const data = {
      name_category: name,
    };

    const response = await fetch('/admin/categories/add_category', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    console.log(result);
  }
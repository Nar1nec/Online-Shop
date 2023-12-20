 async function buyProduct(product_id) {
        const response = await fetch(`/cart/add_to_cart/${product_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    });

        if (response.ok) {
            console.log('Product added to cart successfully');
            // Обновите страницу или выполните другие необходимые действия
        } else {
            console.error('Failed to add product to cart');
            // Обработайте ошибку, если необходимо
        }
    }
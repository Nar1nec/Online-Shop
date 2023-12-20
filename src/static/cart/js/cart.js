async function removeFromCart(item_id) {
    try {
        const response = await fetch(`/cart/remove_from_cart/${item_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            console.log('Item removed from cart successfully');
            // Обновление данных корзины
             location.reload();
        } else {
            console.error('Failed to remove item from cart');
        }
    } catch (error) {
        console.error('Unexpected error:', error);
    }
}

    // Функция для обновления общей стоимости
    function updateTotalPrice() {
        let total = 0;
        document.querySelectorAll('.product-block').forEach(item => {
            const quantity = parseInt(item.querySelector('.quantity').innerText);
            const price = parseFloat(item.querySelector('.price').innerText);
            total += quantity * price;
        });
        document.getElementById('total-price').innerText = `Общая стоимость товаров: ${total.toFixed(2)} руб.`;
    }

    // Вызываем функцию при загрузке страницы и при изменении корзины
    document.addEventListener('DOMContentLoaded', updateTotalPrice);
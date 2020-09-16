document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('id_ordering');

    if (select) {
        select.addEventListener('change', () => {
            select.closest('form').submit();
        })
    }
});

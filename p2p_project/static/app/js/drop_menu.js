const dropdowns = document.querySelectorAll('.dropdown')

dropdowns.forEach (dropdown => {
    let select = dropdown.querySelector ('.select');
    let caret = dropdown.querySelector ('.caret');
    let menu = dropdown.querySelector ('.drop_menu');
    let options = dropdown.querySelectorAll ('.drop_menu li');
    let selected = dropdown.querySelector ('.selected');

    select.addEventListener('click', () => {
        select.classList.toggle('select-clicked');
        caret.classList.toggle('caret-rotate');
        menu.classList.toggle('drop_menu-open');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            selected.innerText = option.innerText;
            select.classList.remove ('select-clicked');
            caret.classList.remove ('caret-rotate');
            menu.classList.remove ('drop_menu-open');

            options.forEach(option => {
                option.classList.remove('active');
            });
            option.classList.add('active');
        });
    });
});

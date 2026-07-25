document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll(
        '[data-bs-toggle="popover"]'
    );

    elements.forEach((element) => {
        new bootstrap.Popover(element);
    });
});

document.querySelectorAll(".schedule-empty-cell").forEach(cell => {

    cell.addEventListener("click", () => {

        const person = cell.dataset.person;
        const date = cell.dataset.date;

        window.location.href =
            `/vacations/create/?person=${person}&date_from=${date}`;

    });

});

let startCell = null;
let selecting = false;

document.querySelectorAll(".schedule-empty-cell").forEach(cell => {

    cell.addEventListener("mousedown", e => {

        selecting = true;
        startCell = cell;

        document
            .querySelectorAll(".schedule-selecting")
            .forEach(c => c.classList.remove("schedule-selecting"));

        cell.classList.add("schedule-selecting");

        e.preventDefault();

    });

    cell.addEventListener("mouseenter", () => {

        if (!selecting || !startCell)
            return;

        if (cell.dataset.person !== startCell.dataset.person)
            return;

        const cells = [...document.querySelectorAll(
            `.schedule-empty-cell[data-person="${cell.dataset.person}"]`
        )];

        const start = cells.indexOf(startCell);
        const end = cells.indexOf(cell);

        const from = Math.min(start, end);
        const to = Math.max(start, end);

        document
            .querySelectorAll(".schedule-selecting")
            .forEach(c => c.classList.remove("schedule-selecting"));

        for (let i = from; i <= to; i++) {
            cells[i].classList.add("schedule-selecting");
        }

    });

});

document.addEventListener("mouseup", () => {

    if (!selecting || !startCell)
        return;

    selecting = false;

    const selected = document.querySelectorAll(".schedule-selecting");

    if (!selected.length)
        return;

    const first = selected[0];
    const last = selected[selected.length - 1];

    window.location.href =
        `/vacations/create/?person=${first.dataset.person}` +
        `&date_from=${first.dataset.date}` +
        `&date_to=${last.dataset.date}`;

});
document.querySelectorAll(".schedule-empty-cell").forEach(cell => {

    cell.addEventListener("click", () => {

        const person = cell.dataset.person;
        const date = cell.dataset.date;

        window.location.href =
            `/vacations/create/?person=${person}&date_from=${date}&date_to=${date}`;

    });

});
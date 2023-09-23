/* Sorting tables */
id_table.onclick = function (e) {
  if (e.target.tagName != 'TH') return;
  let th = e.target;
  sortTable(th.cellIndex, th.dataset.type, 'id_table');
};

function sortTable(colNum, type, id) {
  let elem = document.getElementById(id)
  let tbody = elem.querySelector('tbody');
  let rowsArray = Array.from(tbody.rows);
  let compare;
  switch (type) {
    case 'number':
      compare = function (rowA, rowB) {
        return rowA.cells[colNum].innerHTML - rowB.cells[colNum].innerHTML;
      };
      break;
    case 'string':
      compare = function (rowA, rowB) {
        return rowA.cells[colNum].innerHTML > rowB.cells[colNum].innerHTML ? 1 : -1;
      };
      break;
  }
  rowsArray.sort(compare);
  tbody.append(...rowsArray);
}



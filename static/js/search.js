const searchInput = document.querySelector('.search');
const selectOptions = document.querySelector('.disease-search');
const options = selectOptions.options;

searchInput.addEventListener('keydown', function() {
  const searchTerm = this.value.toLowerCase();
  for (let i = 0; i < options.length; i++) {
    const option = options[i];
    if (option.text.toLowerCase().includes(searchTerm)) {
      option.style.display = 'block';
    } else {
      option.style.display = 'none';
    }
  }
  selectOptions.style.display = 'block';
});

document.addEventListener('click', function(event) {
  if (!event.target.closest('.custom-select')) {
    selectOptions.style.display = 'none';
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const openBtn = document.getElementById("openModalBtn");
  const modal = document.getElementById("hanjaModal");
  const hanjaForm = document.getElementById("hanjaSelectForm");
  const nameInput = document.getElementById("name");
  const selectedHanjaDisplay = document.getElementById("selected_hanja");
  const confirmBtn = document.getElementById("confirmHanjaBtn");

  openBtn.addEventListener("click", function () {
    const name = nameInput.value.trim();
    if (name.length < 2 || name.length > 4) {
      alert("이름은 2~4자만 가능합니다.");
      return;
    }

    fetch(`/estimate/ajax/hanja/?name=${encodeURIComponent(name)}`)
      .then((response) => response.json())
      .then((data) => {
        if (!hanjaForm) {
          console.error("hanjaSelectForm 요소가 없습니다!");
          return;
        }

        hanjaForm.innerHTML = "";

        data.data.forEach((candidates, index) => {
          const label = document.createElement("label");
          label.innerText = `${index + 1}번째 글자`;
          hanjaForm.appendChild(label);

          const select = document.createElement("select");
          select.name = `hanja_${index}`;
          select.classList.add("h-10", "pl-3", "text-lg");

          candidates.forEach((hanja) => {
            const option = document.createElement("option");
            option.value = hanja.char;
            option.text = `${hanja.char} - ${hanja.main_mean}`;
            select.appendChild(option);
          });

          hanjaForm.appendChild(select);
        });

        modal.classList.remove("hidden");
      });
  });

  confirmBtn.addEventListener("click", function () {
    const selects = document.querySelectorAll("#hanjaSelectForm select");
    let result = "";
    selects.forEach((select) => {
      result += select.value;
    });
    selectedHanjaDisplay.innerText = `선택한 한자 이름 : ${result}`;
    document.getElementById('name_hanja').value = result;
    modal.classList.add("hidden");
  });
});

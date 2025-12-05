// product data
const stones = [
  {
    id: "amethyst",
    name: { ru: "Аметист", en: "Amethyst" },
    price: 37,
    image: "images/amethyst.JPG",
    desc: {
      ru: "Камень спокойствия и интуиции.",
      en: "Stone of calm and intuition."
    },
    zodiac: ["pisces", "aquarius", "virgo"]
  },
  {
    id: "citrine",
    name: { ru: "Цитрин", en: "Citrine" },
    price: 35,
    image: "images/citrine.JPG",
    desc: {
      ru: "Камень радости и удачи.",
      en: "Stone of joy and luck."
    },
    zodiac: ["leo", "gemini", "aries"]
  },
  {
    id: "coral",
    name: { ru: "Корал", en: "Coral" },
    price: 29,
    image: "images/coral.jpg",
    desc: {
      ru: "Камень жизненной энергии и творчества.",
      en: "Stone of life energy and creativity."
    },
    zodiac: ["aries", "leo", "pisces"]
  },
  {
    id: "garnet",
    name: { ru: "Гранат", en: "Garnet" },
    price: 33,
    image: "images/garnet.jpg",
    desc: {
      ru: "Камень страсти и мотивации.",
      en: "Stone of passion and motivation."
    },
    zodiac: ["scorpio", "aries", "capricorn"]
  },
  {
    id: "tiger-eye",
    name: { ru: "Тигровый глаз", en: "Tiger’s Eye" },
    price: 40,
    image: "images/tiger-eye.jpg",
    desc: {
      ru: "Камень фокуса, уверенности и защиты.",
      en: "Stone of focus, confidence and protection."
    },
    zodiac: ["leo", "gemini", "virgo"]
  },
  {
    id: "lapis",
    name: { ru: "Лазурит", en: "Lapis Lazuli" },
    price: 35,
    image: "images/lapis.JPG",
    desc: {
      ru: "Камень честности и мудрости.",
      en: "Stone of honesty and wisdom."
    },
    zodiac: ["sagittarius", "aquarius", "pisces"]
  },
  {
    id: "jade",
    name: { ru: "Нефрит", en: "Jade" },
    price: 28,
    image: "images/jade.JPG",
    desc: {
      ru: "Камень стабильности и гармонии.",
      en: "Stone of stability and harmony."
    },
    zodiac: ["taurus", "virgo", "libra"]
  },
  {
    id: "malachite",
    name: { ru: "Малахит", en: "Malachite" },
    price: 34,
    image: "images/malachite.jpg",
    desc: {
      ru: "Камень трансформации и защиты.",
      en: "Stone of transformation and protection."
    },
    zodiac: ["scorpio", "capricorn", "pisces"]
  },
  {
    id: "labradorite",
    name: { ru: "Лабрадорит", en: "Labradorite" },
    price: 31,
    image: "images/labradorite.jpg",
    desc: {
      ru: "Камень интуиции и перемен.",
      en: "Stone of intuition and change."
    },
    zodiac: ["scorpio", "aquarius", "pisces"]
  },
  {
    id: "turquoise",
    name: { ru: "Фируза", en: "Turquoise" },
    price: 29,
    image: "images/turquoise.JPG",
    desc: {
      ru: "Камень защиты, баланса и удачи.",
      en: "Stone of protection, balance and luck."
    },
    zodiac: ["sagittarius", "pisces", "aquarius"]
  },
  {
    id: "moonstone",
    name: { ru: "Лунный камень", en: "Moonstone" },
    price: 31,
    image: "images/moonstone.jpg",
    desc: {
      ru: "Камень женской энергии и интуиции.",
      en: "Stone of feminine energy and intuition."
    },
    zodiac: ["cancer", "pisces", "capricorn"]
  },
  {
    id: "obsidian",
    name: { ru: "Обсидиан", en: "Obsidian" },
    price: 29,
    image: "images/obsidian.jpg",
    desc: {
      ru: "Мощный защитный камень.",
      en: "Strong protective stone."
    },
    zodiac: ["scorpio", "capricorn", "sagittarius"]
  },
  {
    id: "jasper",
    name: { ru: "Яшма", en: "Jasper" },
    price: 27,
    image: "images/jasper.jpg",
    desc: {
      ru: "Камень спокойствия и внутренней силы.",
      en: "Stone of calm and inner strength."
    },
    zodiac: ["aries", "virgo", "scorpio"]
  },
  {
    id: "rose-quartz",
    name: { ru: "Розовый кварц", en: "Rose Quartz" },
    price: 27,
    image: "images/rose-quartz.jpg",
    desc: {
      ru: "Камень любви и мягкости.",
      en: "Stone of love and gentleness."
    },
    zodiac: ["cancer", "taurus", "libra"]
  },
  {
    id: "brooch",
    name: { ru: "Брошь", en: "Brooch" },
    price: 30,
    image: "images/brooch.JPG",
    desc: {
      ru: "Аксессуар ручной работы.",
      en: "Handmade accessory."
    },
    zodiac: []
  },
  {
    id: "keychain",
    name: { ru: "Брелок", en: "Keychain" },
    price: 25,
    image: "images/keychain.JPG",
    desc: {
      ru: "Декоративный брелок для привлечения финансового изобилия.",
      en: "Decorative keychain to attract financial abundance."
    },
    zodiac: []
  }
];

// zodiac sign names
const zodiacNames = {
  ru: {
    aries: "Овен",
    taurus: "Телец",
    gemini: "Близнецы",
    cancer: "Рак",
    leo: "Лев",
    virgo: "Дева",
    libra: "Весы",
    scorpio: "Скорпион",
    sagittarius: "Стрелец",
    capricorn: "Козерог",
    aquarius: "Водолей",
    pisces: "Рыбы"
  },
  en: {
    aries: "Aries",
    taurus: "Taurus",
    gemini: "Gemini",
    cancer: "Cancer",
    leo: "Leo",
    virgo: "Virgo",
    libra: "Libra",
    scorpio: "Scorpio",
    sagittarius: "Sagittarius",
    capricorn: "Capricorn",
    aquarius: "Aquarius",
    pisces: "Pisces"
  }
};

// UI text for RU / EN
const uiText = {
  ru: {
    subtitle: "Каталог украшений из натуральных камней",
    sortLabel: "Сортировка:",
    filterLabel: "Фильтр по знаку:",
    filterAll: "Все знаки",
    cartTitle: "Корзина",
    cartEmpty: "Корзина пуста",
    cartTotalLabel: "Итого:",
    addButton: "В корзину"
  },
  en: {
    subtitle: "Jewelry catalog with natural gemstones",
    sortLabel: "Sort:",
    filterLabel: "Filter by sign:",
    filterAll: "All signs",
    cartTitle: "Cart",
    cartEmpty: "Cart is empty",
    cartTotalLabel: "Total:",
    addButton: "Add to cart"
  }
};

const grid = document.getElementById("grid");
const sortSel = document.getElementById("sort");
const zodiacSel = document.getElementById("zodiac");
const langSel = document.getElementById("lang");

const cartItemsEl = document.getElementById("cart-items");
const cartCountEl = document.getElementById("cart-count");
const cartTotalEl = document.getElementById("cart-total");

let currentLang = "ru";
const cart = {};

// format zodiac list as a readable string
function formatZodiacList(arr) {
  if (!arr || arr.length === 0) return "";
  return arr.map(z => zodiacNames[currentLang][z]).join(", ");
}

// render catalog grid
function renderCatalog(list) {
  grid.innerHTML = "";
  list.forEach(stone => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <div class="imgwrap">
        <img src="${stone.image}" alt="${stone.name[currentLang]}">
      </div>
      <div class="body">
        <div class="topline">
          <div class="name">${stone.name[currentLang]}</div>
          <div class="price">${stone.price} AZN</div>
        </div>
        <div class="details">
          ${stone.desc[currentLang]}${
            stone.zodiac.length
              ? "<br><b>" + formatZodiacList(stone.zodiac) + "</b>"
              : ""
          }
        </div>
        <button class="add-btn" data-id="${stone.id}" data-text-btn="addButton">
          ${uiText[currentLang].addButton}
        </button>
      </div>
    `;

    // toggle description on card click
    card.addEventListener("click", () => {
      card.classList.toggle("open");
    });

    // add to cart on button click (without toggling description)
    const btn = card.querySelector(".add-btn");
    btn.addEventListener("click", e => {
      e.stopPropagation();
      addToCart(stone.id);
    });

    grid.appendChild(card);
  });
}

// fill zodiac filter select from product data
function fillZodiacFilter() {
  const set = new Set();
  stones.forEach(s => s.zodiac.forEach(z => set.add(z)));

  const prev = zodiacSel.value || "all";
  zodiacSel.innerHTML = "";

  const optAll = document.createElement("option");
  optAll.value = "all";
  optAll.textContent = uiText[currentLang].filterAll;
  zodiacSel.appendChild(optAll);

  [...set].sort().forEach(code => {
    const o = document.createElement("option");
    o.value = code;
    o.textContent = zodiacNames[currentLang][code];
    zodiacSel.appendChild(o);
  });

  if (prev && (prev === "all" || set.has(prev))) {
    zodiacSel.value = prev;
  }
}

// apply selected filter and sort, then re-render catalog
function applyFilters() {
  let list = [...stones];
  const z = zodiacSel.value;

  if (z && z !== "all") {
    list = list.filter(s => s.zodiac.includes(z));
  }

  if (sortSel.value === "price-asc") {
    list.sort((a, b) => a.price - b.price);
  } else if (sortSel.value === "price-desc") {
    list.sort((a, b) => b.price - a.price);
  } else if (sortSel.value === "name-asc") {
    list.sort((a, b) =>
      a.name[currentLang].localeCompare(b.name[currentLang])
    );
  }

  renderCatalog(list);
}

// add item to cart (increase quantity)
function addToCart(id) {
  cart[id] = (cart[id] || 0) + 1;
  renderCart();
}

// render cart with remove buttons
function renderCart() {
  const entries = Object.entries(cart);
  cartItemsEl.innerHTML = "";

  if (entries.length === 0) {
    cartItemsEl.textContent = uiText[currentLang].cartEmpty;
    cartCountEl.textContent = 0;
    cartTotalEl.textContent = "0 AZN";
    return;
  }

  let total = 0;
  let count = 0;

  entries.forEach(([id, qty]) => {
    const item = stones.find(x => x.id === id);
    if (!item) return;

    total += item.price * qty;
    count += qty;

    const row = document.createElement("div");
    row.className = "cart-item-row";
    row.innerHTML = `
      <div class="cart-item-name">${item.name[currentLang]}</div>
      <div class="cart-item-qty">×${qty} · ${item.price} AZN</div>
      <button class="cart-remove" data-id="${id}">
        ${currentLang === "ru" ? "Удалить" : "Remove"}
      </button>
    `;

    cartItemsEl.appendChild(row);
  });

  cartCountEl.textContent = count;
  cartTotalEl.textContent = total + " AZN";

  // attach listeners to "Remove" buttons
  cartItemsEl.querySelectorAll(".cart-remove").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-id");
      delete cart[id];
      renderCart();
    });
  });
}

// language switch
function updateLang() {
  currentLang = langSel.value;

  // update static UI text
  document.querySelectorAll("[data-text]").forEach(el => {
    const key = el.getAttribute("data-text");
    el.textContent = uiText[currentLang][key];
  });

  // update filter options and catalog
  fillZodiacFilter();
  applyFilters();

  // update cart texts
  renderCart();

  // update "add to cart" buttons
  document.querySelectorAll("[data-text-btn]").forEach(el => {
    const key = el.getAttribute("data-text-btn");
    el.textContent = uiText[currentLang][key];
  });
}

// initial render
fillZodiacFilter();
applyFilters();
renderCart();

// event listeners
sortSel.addEventListener("change", applyFilters);
zodiacSel.addEventListener("change", applyFilters);
langSel.addEventListener("change", updateLang);

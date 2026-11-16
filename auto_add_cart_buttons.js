/**
 * Domel Konin – automatycznie dodaje przycisk "Dodaj do koszyka"
 * na kartach produktów, które go jeszcze nie mają.
 * Działa z cart.js (data-add-to-cart).
 */
(function () {
  function addButtons() {
    document.querySelectorAll(".product-card").forEach(function (card) {
      if (card.querySelector("[data-add-to-cart]")) return;

      var h3 = card.querySelector("h3");
      var cenaEl = card.querySelector(".cena");
      var title = (h3 && h3.textContent.trim()) || "Produkt";
      var price = (cenaEl && cenaEl.textContent.trim()) || "Cena na zapytanie";

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn-add-cart";
      btn.setAttribute("data-add-to-cart", "");
      btn.setAttribute("data-title", title);
      btn.setAttribute("data-price", price);
      btn.innerHTML = '<i class="fa-solid fa-cart-plus"></i> Dodaj do koszyka';

      if (cenaEl && cenaEl.parentNode) {
        cenaEl.insertAdjacentElement("afterend", btn);
      } else {
        card.appendChild(btn);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addButtons);
  } else {
    addButtons();
  }
})();

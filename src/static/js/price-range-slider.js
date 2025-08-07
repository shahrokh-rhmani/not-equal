document.addEventListener('DOMContentLoaded', function () {
    const priceRange = document.getElementById('price-range');
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');

    // Initialize with current values or defaults
    const minPrice = parseInt(minPriceInput.value) || 0;
    const maxPrice = parseInt(maxPriceInput.value) || 1000000;

    // Create slider
    noUiSlider.create(priceRange, {
        start: [minPrice, maxPrice],
        connect: true,
        direction: 'rtl',
        range: {
            'min': 0,
            'max': 1000000
        },
        step: 1,
        tooltips: [true, true],
        format: wNumb({
            decimals: 0,
            thousand: ',',
            suffix: ' تومان'
        })
    });

    // Update input fields when slider changes
    priceRange.noUiSlider.on('update', function (values, handle) {
        const value = values[handle];
        if (handle) {
            maxPriceInput.value = value.replace(/[^0-9]/g, '');
        } else {
            minPriceInput.value = value.replace(/[^0-9]/g, '');
        }
    });

    // Update slider when input fields change
    function updateSliderFromInputs() {
        let minValue = parseInt(minPriceInput.value) || 0;
        let maxValue = parseInt(maxPriceInput.value) || 1000000;

        // Validate values
        if (minValue < 0) minValue = 0;
        if (maxValue > 1000000) maxValue = 1000000;
        if (minValue > maxValue) {
            // If the minimum value becomes greater than the maximum, set the minimum value equal to the maximum
            minValue = maxValue;
            minPriceInput.value = minValue;
        }

        // Update slider
        priceRange.noUiSlider.set([minValue, maxValue]);
    }

    // Add event listeners for input changes
    minPriceInput.addEventListener('change', updateSliderFromInputs);
    maxPriceInput.addEventListener('change', updateSliderFromInputs);

    // Also update on input (real-time) with debounce
    let timeout;
    function debounceUpdate() {
        clearTimeout(timeout);
        timeout = setTimeout(updateSliderFromInputs, 500);
    }

    minPriceInput.addEventListener('input', debounceUpdate);
    maxPriceInput.addEventListener('input', debounceUpdate);
});
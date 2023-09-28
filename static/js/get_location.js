// Makes AJAX requests to the server to change the dropdown selection behavior
// of the country, region, and city fields in the update profile form
// based on the user's selections


$(document).ready(function () {
    // Trigger search on dropdown when it is opened
    $('.select2').on('select2:open', function () {
        $(this).data('select2').dropdown.$search.focus();
    });

    // Get the form and fields
    const form = $('#updateProfileForm');
    const countryField = form.find('#id_country').addClass('country-select2');
    const regionField = form.find('#id_region').addClass('region-select2');
    const cityField = form.find('#id_city').addClass('city-select2');

    // Initialize Select2 library on the country, region, and city fields
    // with the .select2 class attribute
    $('.country-select2').select2({
        dropdownAutoWidth: true,
        width: '100%',
        dropdownParent: $('#updateProfileForm'),
        focus: true,
        placeholder: 'Select a Country',
        allowClear: true,
    });

    $('.region-select2').select2({
        dropdownAutoWidth: true,
        width: '100%',
        dropdownParent: $('#updateProfileForm'),
        focus: true,
        placeholder: 'Select a Region',
        allowClear: true,
    });

    $('.city-select2').select2({
        dropdownAutoWidth: true,
        width: '100%',
        dropdownParent: $('#updateProfileForm'),
        focus: true,
        placeholder: 'Select a City',
        allowClear: true,
    });


    // Disable region and city fields initially
    regionField.prop('disabled', true);
    cityField.prop('disabled', true);

    // Handle country field change event
    countryField.on('change', function () {
        const countryId = $(this).val();
        if (countryId) {
            // Fetch regions for the selected country
            $.getJSON('/profiles/get_regions/', { country_id: countryId }, function (data) {
                // Clear and enable the region field
                regionField.empty().prop('disabled', false);
                console.log(data);
                // Populate the region field with options
                $.each(data.regions, function (index, region) {
                    regionField.append('<option value="' + region.id + '">' + region.name + '</option>');
                });

                // Clear and disable the city field
                cityField.val('').prop('disabled', true);
            });
        } else {
            // Clear and disable the region and city fields if no country is selected
            regionField.val('').prop('disabled', true);
            cityField.val('').prop('disabled', true);
        }
    });

    // Handle region field change event
    regionField.on('change', function () {
        const regionId = $(this).val();
        if (regionId) {
            // Fetch cities for the selected region
            $.getJSON('/profiles/get_cities/', { region_id: regionId }, function (data) {
                // Clear and enable the city field
                cityField.empty().prop('disabled', false);

                // Populate the city field with options
                $.each(data.cities, function (index, city) {
                    cityField.append('<option value="' + city.id + '">' + city.name + '</option>');
                });
            });
        } else {
            // Clear and disable the city field if no region is selected
            cityField.val('').prop('disabled', true);
        }
    });

    // Trigger country change event on page load
    countryField.change();
});


/**
 *  @file   organism_search.js
 *  @brief  add Ajax support and event handlers to home page search form
 *  @author Kevin Ernst <ernstki -at- mail.uc.edu>
 */

$(function() {

  // jQuery selectors for the elements we'll need below
  SEARCH_FORM    = $('#search-form');
  SEARCH_RESULTS = $('#search-results');
  SEARCH_INPUT   = $('#search-input');
  RESET_BUTTON   = $('#search-reset');

  function shortOrg(name) {
    var a = name.split(' ');
    if (a.length === 1) return name;
    return a[0].replace(/(\w).*/, '$1.') + ' ' + a[1];
  }

  function byTextLabel(a, b) {
    if (a.text  <  b.text) return -1;
    if (a.text  >  b.text) return 1;
    if (a.text === b.text) return 0;
  }

  // Bind the Select2 library to the 'search-input' field
  SEARCH_INPUT.select2({
    ajax: {
      url: $API_ROOT + 'api/v1/organism/autocomplete',
      dataType: 'json',
      delay: 250,
      // This seems to be necessary (to label the actual results from
      // the API with a 'results' key) otherwise you get an error message
      // with 'debug: true' that's "data is undefined" or "results key
      // is empty" or something like that.
      processResults: function (data) {
        data.forEach(function(item) {
          item.text = shortOrg(item.text);
        });
        return { results: data.sort(byTextLabel) };
      },
      cache: true,
    },
    theme: 'bootstrap',
    placeholder: "Organism or name of clade (e.g., 'mus musculus')",
    placeholderOption: 'first',
    //debug: true
  });

  // Update the 'search-results' textarea with results of searching the
  // 'organisms' table for whatever's in the 'search-input' field
  SEARCH_FORM.submit(function(e) {
    e.preventDefault();
    var inputs = $(this).serializeArray();
    $('#search-results').text(''); // empty the results textarea

    inputs.forEach(function(item) {
      if (item.name !== 'search-input') return;
      // might be useful to see if item.value is actually an integer...
      $.ajax({
          url: $API_ROOT + 'api/v1/organism/' + item.value,
          dataType: 'json',
          cache: true,
          success: function updateSearchText(data, status) {
            var resultText = SEARCH_RESULTS.text();
            resultText += data.id + ": " + data.name + "\n";
            SEARCH_RESULTS.text(resultText);
          }
      }); // ajax
    }); // forEach

  }); // #search-form.click

  // Reset the search form
  RESET_BUTTON.click(function(e) {
    SEARCH_RESULTS.text('');
    SEARCH_INPUT.val(null).trigger("change");
  });

}); // document.ready

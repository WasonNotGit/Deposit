      $("#o_field_input_19").suggestions({
          token: "979083f3c2cbf99e6de693f11ec59e1ff63da6e6",
          type: "ADDRESS",
          count: 5,
          /* Вызывается, когда пользователь выбирает одну из подсказок */
          onSelect: function(suggestion) {
              console.log(suggestion);
          }
      });


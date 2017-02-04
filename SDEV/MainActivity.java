package gatech.edu.assignment_4;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void handleClick(View v) {
        EditText entrantsfee = (EditText) findViewById(R.id.entrantsFee);
        EditText housecut = (EditText) findViewById(R.id.houseCutValue);
        EditText entrantsnum = (EditText) findViewById(R.id.entrantsNumber);
        EditText housepercent = (EditText) findViewById(R.id.housePercentage);
        EditText firsttext = (EditText) findViewById(R.id.firstPrizeValue);
        EditText secondtext = (EditText) findViewById(R.id.secondPrizeValue);
        EditText thirdtext = (EditText) findViewById(R.id.thirdPrizeValue);

        //Data Validation - Check for empty
        boolean isAnyEmpty = false;
        if (TextUtils.isEmpty(entrantsfee.getText())) {
            entrantsfee.setError("Invalid Fee");
            isAnyEmpty = true;

        }if(TextUtils.isEmpty(entrantsnum.getText())) {
            entrantsnum.setError("Invalid Number of Entrants");
            isAnyEmpty = true;

        }if(TextUtils.isEmpty(housepercent.getText())){
            housepercent.setError("Invalid House Percentage");
            isAnyEmpty = true;
        } if(isAnyEmpty == false) {
            String fee = entrantsfee.getText().toString();
            double fee1 = Double.parseDouble(fee);

            String entrants = entrantsnum.getText().toString();
            double entrants1 = Double.parseDouble(entrants);

            String percent = housepercent.getText().toString();
            double percent1 = Double.parseDouble(percent);


            if (entrants1 <= 3) {
                entrantsnum.setError("Invalid Number of Entrants");

            } else if (percent1 < 0 || percent1 > 100) {
                housepercent.setError("Invalid House Percentage");

            } else {
                int output = (int) (fee1 * entrants1 * percent1 / 100.0);

                String outtext = String.valueOf(output);
                housecut.setText(outtext);

                double leftover = (fee1 * entrants1 * (100.0 - percent1) / 100.0);
                int first = (int) (leftover * 0.5);
                int second = (int) (leftover * 0.3);
                int third = (int) (leftover * 0.2);
                String firstString = String.valueOf(first);
                String secondString = String.valueOf(second);
                String thirdString = String.valueOf(third);

                firsttext.setText(firstString);
                secondtext.setText(secondString);
                thirdtext.setText(thirdString);
            }

        }
    }
}

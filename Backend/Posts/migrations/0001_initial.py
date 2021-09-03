# Generated by Django 3.2.6 on 2021-09-02 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Profile', '0002_alter_profile_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField(default=0)),
                ('title', models.CharField(default='', max_length=30)),
                ('description', models.CharField(default='', max_length=250)),
                ('price', models.IntegerField(blank=True, default='', null=True)),
                ('year', models.IntegerField(choices=[(1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], default=2021, verbose_name='year')),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='static/profile')),
                ('time', models.TimeField(auto_now=True)),
                ('date', models.DateField(auto_now=True)),
                ('is_donate', models.BooleanField(default=False)),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Profile.profile')),
            ],
        ),
    ]
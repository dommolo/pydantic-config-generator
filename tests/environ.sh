read -p "Enter the radius: " RADIUS
read -p "Enter the border color: " BORDER_COLOR
read -p "Enter the fill color: " FILL_COLOR
read -p "Enter the text: " TEXT

export RADIUS=$RADIUS
export BORDER_COLOR=$BORDER_COLOR
export FILL_COLOR=$FILL_COLOR
export TEXT=$TEXT

python environ.py

cat config.ini
/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

package piclock;

import javax.swing.*;
import java.awt.*;
import java.util.*;
import java.time.*;
import java.time.format.*;

/**
 *
 * @author rizwan
 */
public class Canvas extends JPanel {
    String timeUntilRangeEnd(String range) {
        String endStr = range.split("-")[1].trim();

        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("hh:mm a");
        LocalTime target = LocalTime.parse(endStr, fmt);

        LocalTime now = LocalTime.now();

        if (target.isBefore(now)) {
            target = target.plusHours(24);
        }

        Duration d = Duration.between(now, target);

        long totalSeconds = d.getSeconds();
        long minutes = Math.max(0, totalSeconds / 60);
        long seconds = Math.max(0, totalSeconds % 60)+1;

        return String.format("%02d:%02d", minutes, seconds);
    }
    void drawCenteredString(Graphics2D g2, String text, int cx, int cy) {
        /*
         *  Because text sucks.
         */
        FontMetrics fm = g2.getFontMetrics();
        int x = cx - fm.stringWidth(text) / 2;
        int y = cy + fm.getAscent() / 2;
        g2.drawString(text, x, y);
    }
    
    void drawCenteredStringFit(Graphics2D g2, String text, int cx, int cy, int maxWidth, float startingFontSize) {
        // Save the original font
        Font originalFont = g2.getFont();
        Font font = originalFont.deriveFont(startingFontSize);
        g2.setFont(font);

        FontMetrics fm = g2.getFontMetrics(font);

        // Shrink font until text fits
        while (fm.stringWidth(text) > maxWidth && font.getSize() > 5) {
            font = font.deriveFont((float)(font.getSize() - 1));
            g2.setFont(font);
            fm = g2.getFontMetrics(font);
        }

        // Draw centered
        int x = cx - fm.stringWidth(text) / 2;
        int y = cy + fm.getAscent() / 2;
        g2.drawString(text, x, y);

        // Restore the original font
        g2.setFont(originalFont);
    }
    @Override
    protected void paintComponent(Graphics g){
        Server.selectDisplay();
        super.paintComponent(g);
        int w = getWidth();
        int h = getHeight();
        double yShift = 13.0 * h / 507.0; // vertical shift

        Graphics2D cv = (Graphics2D) g;
        cv.setFont(new Font("DejaVu Sans", Font.PLAIN, 20*Math.min(w,h)/500));

        // 1. Background
        Image bg = new ImageIcon(
            getClass().getResource("/piclock/assets/bg.png")
        ).getImage();
        cv.drawImage(bg, 0, 0, w, h, this);
        cv.setColor(new Color(0, 112, 198, 64));
        cv.fillRoundRect((int)(60*w/900.0),(int)(5*h/507.0+yShift),(int)(770*w/900.0), (int)(470*h/507.0), 26, 26);

        // 2. Clock
        //    1. Frame
        cv.setColor(new Color(201, 231, 238, 127));
        cv.fillOval(w/7-3, (int)(h/6-3+yShift), Math.min(w,h)/2+6, Math.min(w,h)/2+6);
        //    2. Inner frame
        cv.setColor(new Color(78, 170, 223, 127));
        cv.fillOval(w/7+4, (int)(h/6+4+yShift), (Math.min(w,h)/2)-8, (Math.min(w,h)/2)-8);
        //    3. Deeper frame
        cv.setColor(new Color(0, 0, 26, 191));
        cv.fillOval(w/7+6, (int)(h/6+6+yShift), (Math.min(w,h)/2)-12, (Math.min(w,h)/2)-12);
        //    4. Numbers
        cv.setColor(new Color(201, 231, 238));
        int cx = w/7+Math.min(w,h)/4;
        int cy = h/6+Math.min(w,h)/4 + (int)yShift;
        String[] numbers = {"12","1","2","3","4","5","6","7","8","9","10","11"};
        FontMetrics fm = cv.getFontMetrics();
        int textHeight = fm.getAscent();
        int radius = (int)(Math.min(w, h) / 4.375 - textHeight);
        for (int i = 0; i < 12; i++) {
            String text = numbers[i];
            double angle = Math.toRadians(30 * i);
            int x = (int)(cx + Math.sin(angle) * radius);
            int y = (int)(cy - Math.cos(angle) * radius);
            int textWidth = fm.stringWidth(text);
            textHeight = fm.getAscent(); 
            int drawX = x - textWidth / 2;
            int drawY = y + textHeight / 2;
            cv.drawString(text, drawX, drawY);
        }

        //   5. Day/Date
        g.setColor(new Color(16639820));
        g.setFont(new Font("DejaVu Sans", Font.PLAIN, 15*Math.min(w,h)/500));
        fm = cv.getFontMetrics();
        Calendar c = Calendar.getInstance();
        String[] days = {"Sun","Mon","Tue","Wed","Thu","Fri","Sat"};
        int dx = cx - fm.stringWidth(days[c.get(Calendar.DAY_OF_WEEK)-1])/2;
        cv.drawString(days[c.get(Calendar.DAY_OF_WEEK)-1],dx,cy+40*Math.min(w,h)/500);
        dx = cx - fm.stringWidth(""+c.get(Calendar.DATE)+" | "+c.get(Calendar.MONTH)+" | "+c.get(Calendar.YEAR))/2;
        cv.drawString(""+c.get(Calendar.DATE)+" | "+(c.get(Calendar.MONTH)+1)+" | "+c.get(Calendar.YEAR),dx,cy+60*Math.min(w,h)/500);

        //   6. Hands        
        cv.setStroke(new BasicStroke((int)(5*w/900.0),BasicStroke.CAP_ROUND,BasicStroke.JOIN_BEVEL));
        cv.setColor(new Color(201, 231, 238));
        cv.drawLine((int)(cx - radius*0.1*Math.sin(Math.toRadians(30*c.get(Calendar.HOUR)+0.5*c.get(Calendar.MINUTE)))), 
                    (int)((cy + radius*0.1*Math.cos(Math.toRadians(30*c.get(Calendar.HOUR)+0.5*c.get(Calendar.MINUTE))))), 
                    (int)(cx + radius*0.5*Math.sin(Math.toRadians(30*c.get(Calendar.HOUR)+0.5*c.get(Calendar.MINUTE)))), 
                    (int)((cy - radius*0.5*Math.cos(Math.toRadians(30*c.get(Calendar.HOUR)+0.5*c.get(Calendar.MINUTE))))));
        cv.drawLine((int)(cx - radius*0.1*Math.sin(Math.toRadians(6*c.get(Calendar.MINUTE)))), 
                    (int)(cy + radius*0.1*Math.cos(Math.toRadians(6*c.get(Calendar.MINUTE)))), 
                    (int)(cx + radius*0.8*Math.sin(Math.toRadians(6*c.get(Calendar.MINUTE)))), 
                    (int)(cy - radius*0.8*Math.cos(Math.toRadians(6*c.get(Calendar.MINUTE)))));
        cv.setColor(new Color(252, 73, 80));
        cv.setStroke(new BasicStroke((int)(2*w/900.0),BasicStroke.CAP_ROUND,BasicStroke.JOIN_BEVEL));
        cv.drawLine((int)(cx - radius*0.2*Math.sin(Math.toRadians(6*c.get(Calendar.SECOND)))), 
                    (int)(cy + radius*0.2*Math.cos(Math.toRadians(6*c.get(Calendar.SECOND)))), 
                    (int)(cx + radius*1.1*Math.sin(Math.toRadians(6*c.get(Calendar.SECOND)))), 
                    (int)(cy - radius*1.1*Math.cos(Math.toRadians(6*c.get(Calendar.SECOND)))));

        //   7. Central knob
        cv.setColor(new Color(50, 50, 50));
        cv.fillOval((int)(cx-radius*0.1/2),(int)(cy-radius*0.1/2), (int)(0.1*radius), (int)(0.1*radius));

        //   8. Lines
        cv.setColor(new Color(201, 231, 238));
        for(int i=0;i<60;i++){
            if(i%5==0){
                cv.setStroke(new BasicStroke((int)(5*w/900.0),BasicStroke.CAP_BUTT,BasicStroke.JOIN_BEVEL));
            } else {
                cv.setStroke(new BasicStroke((int)(w/900.0),BasicStroke.CAP_ROUND,BasicStroke.JOIN_BEVEL));
            }
            cv.drawLine((int)(cx + radius*1.15*Math.sin(Math.toRadians(6*i))), 
                        (int)(cy - radius*1.15*Math.cos(Math.toRadians(6*i))), 
                        (int)(cx + radius*1.2*Math.sin(Math.toRadians(6*i))), 
                        (int)(cy - radius*1.2*Math.cos(Math.toRadians(6*i))));
        }

        // 3. Boxes
        cv.setColor(new Color(125, 191, 177, 85));
        cv.fillRoundRect((int)(450*w/900.0), (int)(14*h/507.0+yShift), (int)(323*w/900.0), (int)(75*h/507.0), 26, 26);
        cv.fillRoundRect((int)(450*w/900.0), (int)(104*h/507.0+yShift), (int)(323*w/900.0), (int)(75*h/507.0), 26, 26);
        cv.fillRoundRect((int)(450*w/900.0), (int)(194*h/507.0+yShift), (int)(323*w/900.0), (int)(75*h/507.0), 26, 26);
        cv.fillRoundRect((int)(100*w/900.0), (int)(380*h/507.0+yShift), (int)(700*w/900.0), (int)(75*h/507.0), 26, 26);

        cv.setColor(new Color(0xffffff));
        cv.fillRect((int)(480*w/900.0), (int)(310*h/507.0+yShift), (int)(285*w/900.0), (int)(20*h/507.0));
        cv.setColor(new Color(0));
        cv.fillRect((int)(481*w/900.0), (int)(311*h/507.0+yShift), (int)(283*w/900.0), (int)(18*h/507.0));

        for(int i=0;i<40;i++){
            cv.setColor(Color.getHSBColor(i/46.0f,1.0f,1.0f));
            cv.fillRect((int)((482+i*7)*w/900.0), (int)(312*h/507.0+yShift), (int)(6*w/900.0), (int)(16*h/507.0));
            if((i/46.0)>Server.sound/120.0){
                break;
            }
        }

        cv.setColor(new Color(125, 191, 177));
        // 4. Icons
        Image teach = new ImageIcon(
            getClass().getResource("/piclock/assets/teach.png")
        ).getImage();
        cv.drawImage(teach, (int)(450*w/900.0), (int)(20*h/507.0+yShift), (int)(88*w/900.0), (int)(72*h/507.0), this);

        Image cal = new ImageIcon(
            getClass().getResource("/piclock/assets/calendar.png")
        ).getImage();
        cv.drawImage(cal, (int)(471*w/900.0), (int)(119*h/507.0+yShift), (int)(61*w/900.0), (int)(62*h/507.0), this);

        Image temp = new ImageIcon(
            getClass().getResource("/piclock/assets/temp.png")
        ).getImage();
        cv.drawImage(temp, (int)(463*w/900.0), (int)(205*h/507.0+yShift), (int)(62*w/900.0), (int)(62*h/507.0), this);

        Image sand = new ImageIcon(
            getClass().getResource("/piclock/assets/time.png")
        ).getImage();
        cv.drawImage(sand, (int)(100*w/900.0), (int)(386*h/507.0+yShift), (int)(61*w/900.0), (int)(71*h/507.0), this);

        // 5. Lines in boxes
        cv.setColor(new Color(201, 231, 238));
        cv.drawLine((int)(545*w/900.0), (int)(56*h/507.0+yShift), (int)(757*w/900.0), (int)(56*h/507.0+yShift));
        cv.drawLine((int)(545*w/900.0), (int)(144*h/507.0+yShift), (int)(757*w/900.0), (int)(144*h/507.0+yShift));
        cv.drawLine((int)(545*w/900.0), (int)(235*h/507.0+yShift), (int)(757*w/900.0), (int)(235*h/507.0+yShift));

        cv.drawLine((int)(450*w/900.0), (int)(400*h/507.0+yShift), (int)(450*w/900.0), (int)(440*h/507.0+yShift));

        // 6. Text
        cv.setFont(new Font("DejaVu Sans", Font.PLAIN, (int)(25*Math.min(w,h)/500.0)));
        cv.setColor(new Color(0xb9cecb));
        drawCenteredStringFit(cv, Server.teacher, (int)(651*w/900.0), (int)(39*h/507.0+yShift), (int)(240*w/900.0), (int)(25*Math.min(w,h)/500.0));
        drawCenteredStringFit(cv, Server.subject, (int)(651*w/900.0), (int)(126*h/507.0+yShift), (int)(240*w/900.0), (int)(25*Math.min(w,h)/500.0));

        cv.setFont(new Font("DejaVu Sans", Font.PLAIN, (int)(20*Math.min(w,h)/500.0)));
        cv.setColor(new Color(0x7fc5ba));
        drawCenteredStringFit(cv, Server.room, (int)(651*w/900.0), (int)(72*h/507.0+yShift), (int)(240*w/900.0), (int)(20*Math.min(w,h)/500.0));
        drawCenteredStringFit(cv, Server.duration, (int)(651*w/900.0), (int)(162*h/507.0+yShift), (int)(240*w/900.0), (int)(20*Math.min(w,h)/500.0));

        cv.setColor(new Color(0xb9cecb));
        drawCenteredString(cv, "Temperature - " + Server.temp + "°C", (int)(651*w/900.0), (int)(218*h/507.0+yShift));

        cv.setColor(new Color(0x7fc5ba));
        drawCenteredString(cv, "Humidity - " + Server.humid + "%", (int)(651*w/900.0), (int)(250*h/507.0+yShift));

        cv.setColor(Server.sound<70?Color.green:new Color(0xfe1212));
        drawCenteredString(cv, "Noise Level: " + (Server.sound<70?(Server.sound+" dB"):("HIGH ("+Server.sound+" dB)")), (int)(622*w/900.0), (int)(290*h/507.0+yShift));

        if(!(Server.event.equals(""))&&(System.currentTimeMillis()%1000<500)){
            cv.setFont(new Font("DejaVu Sans", Font.BOLD, (int)(37*Math.min(w,h)/500.0)));
            cv.setColor(new Color(0xfe1212));
            drawCenteredString(cv, Server.event, (int)(622*w/900.0), (int)(352*h/507.0+yShift));
        }

        cv.setFont(new Font("DejaVu Sans", Font.PLAIN, (int)(25*Math.min(w,h)/500.0)));
        cv.setColor(new Color(0x00e1ff));
        drawCenteredString(cv, "After " + timeUntilRangeEnd(Server.duration)+" minutes", (int)(620*w/900.0), (int)(417*h/507.0+yShift));
        drawCenteredStringFit(cv, "Next Period: "+Server.nextperiod, (int)(295*w/900.0), (int)(417*h/507.0+yShift), (int)(300*w/900.0), 25f * Math.min(w,h)/500.0f);
    }
}
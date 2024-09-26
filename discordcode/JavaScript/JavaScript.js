import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.*;
import net.dv8tion.jda.api.events.interaction.component.ButtonInteractionEvent;
import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.interactions.commands.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.interactions.commands.build.SlashCommandData;

import javax.security.auth.login.LoginException;
import java.io.*;
import java.util.*;

public class a {
    private static final long b = 1238043843476062209L;
    private static final long c = 1002132268736856136L;
    private static final String d = "user_data.txt";
    private static final String e = "MySecurePassword";
    private static final String f = "Patron supporter";
    private boolean g = true;
    private final Map<Long, h> i = new HashMap<>();

    public static void main(String[] args) throws LoginException {
        JDABuilder jdaBuilder = JDABuilder.createDefault("YOUR_BOT_TOKEN");
        jdaBuilder.addEventListeners(new a());
        jdaBuilder.build();
    }

    @Override
    public void onSlashCommandInteraction(SlashCommandInteractionEvent j) {
        switch (j.getName()) {
            case "info":
                k(j);
                break;
            case "toggle_info":
                l(j);
                break;
            case "verify":
                m(j);
                break;
            case "gacha":
                n(j);
                break;
        }
    }

    private void k(SlashCommandInteractionEvent j) {
        if (g) {
            j.reply("開発者<:DEV:1267440009452064829><@1002132268736856136> 開発協力者<:ACCDEV:1267440500625903618> <@1032649313165258772> バージョン<:BE:1267439343882993734><:TA:1267439331069657119>v1")
                .setEphemeral(true).queue();
        } else {
            j.reply("このコマンドは現在無効化されています。").setEphemeral(true).queue();
        }
    }

    private void l(SlashCommandInteractionEvent j) {
        if (j.getUser().getIdLong() == c) {
            g = !g;
            String status = g ? "有効" : "無効";
            j.reply("infoコマンドは現在" + status + "です。").setEphemeral(true).queue();
        } else {
            j.reply("このコマンドを実行する権限がありません。").setEphemeral(true).queue();
        }
    }

    private void m(SlashCommandInteractionEvent j) {
        String o = j.getOption("steam_id").getAsString();
        String p = j.getOption("password").getAsString();

        if (!q(j.getMember())) {
            j.reply("認証できません。必要なロール: " + f).setEphemeral(true).queue();
            return;
        }

        if (!p.equals(e)) {
            j.reply("認証キーが正しくありません。").setEphemeral(true).queue();
            return;
        }

        if (r().contains(o)) {
            j.reply("このSteamIDは既に登録されています。").setEphemeral(true).queue();
            return;
        }

        s(o);
        j.reply("SteamID: " + o + " が登録されました1時間以内に更新されます。").setEphemeral(true).queue();
    }

    private void n(SlashCommandInteractionEvent j) {
        // Implement gacha functionality
    }

    private boolean q(Member j) {
        return j.getRoles().stream().anyMatch(role -> role.getName().equals(f));
    }

    private void s(String o) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(d, true))) {
            writer.write("SteamID: " + o);
            writer.newLine();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private Set<String> r() {
        Set<String> steamIds = new HashSet<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(d))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String steamId = line.split(": ")[1];
                steamIds.add(steamId);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return steamIds;
    }
}

"""The cells and the scores that depend on them hash to a fixed chain."""

from __future__ import annotations

import time
import unittest

from engine.dagapeyeff_provenance import provenance_report


class DagapeyeffProvenanceTest(unittest.TestCase):
    def test_the_chain_reads_the_frozen_scores(self) -> None:
        started = time.perf_counter()
        report = provenance_report()
        self.assertLess(time.perf_counter() - started, 15)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(
            [(entry["name"], entry["content_sha256"]) for entry in report["entries"]],
            [
                ("cells", "f2460a6acdf2f50e12fdc8760c39753746d885282cd0bdfd0eec877c56e6fae5"),
                ("yardstick", "e12910ac3d3d0460db9ce76719298d94f261b7a8a17f09fec675dc4cda635d66"),
                ("balls", "3b84e9af30916cf42181a75d847eff6ba0cc992f606a069fe8fcfc5af0227bdd"),
                ("record", "834058b318779e3811b0b19408329f702bbf3577623dc17912af55c62efc80f7"),
                ("convert", "a64782364904d7e20b9436212d93d90caa172f851d0b0442045943a013c9e549"),
                ("edits", "f662992893d0108c125b14cac1d20a30f7eafe2c58bf6bcc54e9dbc8b5744688"),
                ("corrections", "bf4a749875d9bbd6d318016e7b2a390778d0854257a2e2bb59c3f6acf524d929"),
                ("regroup", "56066cbfba47752377e800bb6816c837c2745467c1a47774fcb162a303a62309"),
                ("keys", "3fe9d3522a1017aa1348f5fa0dd561ccf8940a1bbff5fe6e8246a180c093ae37"),
                ("model", "0d050d25e8e1d2287335f78b6a8e891c0a10a751e9eaa5b7de93bdf7b1e52cf8"),
                ("bifid", "eb196ec222b01a977c3e0694b371af2c97ebae5d6f322aad5e9ddb80804b5c68"),
                ("period4", "932ab042c00b4245c0e68bae71285878574320125580b83ca6e20fee1b48160f"),
                ("word", "ccf44aceb6efea160894fa3730d3cf0e999d5eccdeeebb447e41983867ae8b36"),
                ("running", "1b8674ddd9b6bcb520613739a11188ad3bc623973d24ee603b73b8078d423f33"),
                ("patterns", "c5a700688728c2b918a8c3835ad66f3fc95631500091b122153fc599432a6365"),
                ("columns", "545dc79eab57e4d8457943ca70b90d303b2a3533500f8558aca5b70605aa2492"),
                ("board", "3b39a845596491cb92c951d67d82ce49e5773379c082cc005c978c2a80b527a9"),
                ("infer", "c67768bd2e358814d7b1faea635b909637f2eb2ca249c6053f6889e958c409c0"),
                ("foresight", "48ceb2bf1c6010816c96eb483fccd9dc5609748da14cb459b638f94f94a29e10"),
                ("checks", "4152d21994b7508114c31884edde65a82c728fff00b39b04fd6485a7cdf7099b"),
                ("adversary", "27532401beeff15910f3beb80b6bef2095313b8beb709213f46ee2ce8adede86"),
                ("autokey", "291d0e3ead0bb0903b5a93f7851c44dc9f491060cc3a62a8302759af2a863306"),
                ("digit-routes", "97547066e834b8423c9edee4d893b838baa6b8a22d530d821c0eb2306f1577af"),
                ("angles", "b8a3311101662a1c4d86365b052271bc112878168f513353cbd4845112e061d0"),
                ("delay", "56016bdaf30c3aef8ebcfb956b21a3af8605b88d526667a439d5d476a4765380"),
                ("bookkey", "d62759d707cb9782bc9c138e110b0bbea61d02b7052071be4c4d1e0ff3563184"),
                ("groups", "f80567663cc41f4175fdaa88a8b5fab1306c4bc97069bdc2f158b522c077b1ac"),
                ("places", "142b6e3498c975797e9b5d80f5f3c534e1cbd06a217dc90054d177da2297dfaf"),
                ("solver-swarm", "21509a963f29551ce6155319f60d82e64d1da3d2acbe267c1a4201472779330e"),
                ("classic-swarm", "396a9fa86092731be302bb8243d61f48adde06a54d61dbf8d325d5664c63cfcf"),
                ("router-swarm", "d6539df9419052f5d7137974173ac4d55f5110bea168ddface2c716d84af27a6"),
                ("column-null", "7c9bc0e57380cd289805fe8fc7197982a806d38ab99c4bc74791fa4f7d47a5ac"),
                ("large-swarm", "3cb01d80cd5b96ce4f12e3e08a9c646626159e91ce0f7480e6cf48cff174c327"),
                ("refined-swarm", "b20eb44ed7d876ec239be0dc6df48650350dd6de9d6f4a83516b48bbe3f8c9a4"),
                ("bob-caution", "1abdbfa908bcc9578b9aab1fe7155515e6e632adbff79b019a51b9d9df2beafb"),
                ("keystream", "39ed6e63310f65a30083d55496aab70575823d5f39149402054c6ebf8f7f2bf1"),
                ("depth3", "dbcc65be1cd402f2f1bccbed7a2f264f3f26f6021fa206a3114d01b0b3162785"),
                ("depth4", "7b17d8d9161e3b65ba6f1f8f912bb51efb048a357e85da9a53d88bb20a2a6436"),
                ("placed", "3c57007347fe8c493c3acb252072ef3b107e3e7a26c4ea2b3c08f3532890814f"),
            ],
        )
        self.assertEqual(
            report["chain_sha256"],
            "69a4cd49be55b0c116a9622015ab00838c650377bc416ccef62bce89a28c292a",
        )
        self.assertEqual(report["entries"][0]["chain_sha256"], report["entries"][0]["content_sha256"])
        self.assertNotEqual(report["entries"][1]["chain_sha256"], report["entries"][1]["content_sha256"])


if __name__ == "__main__":
    unittest.main()
